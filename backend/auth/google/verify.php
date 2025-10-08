<?php
require_once '../../config/config.php';

// Ensure API returns clean JSON without HTML error noise
ini_set('display_errors', 0);
ini_set('log_errors', 1);
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);

if (!isset($input['credential'])) {
    echo json_encode(['success' => false, 'error' => 'No credential provided']);
    exit;
}

$credential = $input['credential'];

// Verify the JWT token with Google
$verifyUrl = 'https://oauth2.googleapis.com/tokeninfo?id_token=' . urlencode($credential);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $verifyUrl);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode === 200) {
    $tokenInfo = json_decode($response, true);
    
    // Verify the audience (client ID)
    if ($tokenInfo['aud'] !== GOOGLE_CLIENT_ID) {
        echo json_encode(['success' => false, 'error' => 'Invalid client ID']);
        exit;
    }
    
    // Persist or link user in database
    try {
        $pdo = getPDO();

        // Ensure oauth_user mapping table exists (idempotent create)
        $pdo->exec("CREATE TABLE IF NOT EXISTS oauth_user (
            oauth_user_id INT AUTO_INCREMENT PRIMARY KEY,
            provider VARCHAR(32) NOT NULL,
            provider_user_id VARCHAR(128) NOT NULL,
            student_id INT NOT NULL,
            UNIQUE KEY uq_provider_user (provider, provider_user_id),
            INDEX idx_student (student_id),
            FOREIGN KEY (student_id) REFERENCES student(student_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;");

        $provider = 'google';
        $providerUserId = $tokenInfo['sub'];
        $displayName = isset($tokenInfo['name']) ? $tokenInfo['name'] : '';
        $email = isset($tokenInfo['email']) ? $tokenInfo['email'] : null; // not stored in current schema
        $picture = isset($tokenInfo['picture']) ? $tokenInfo['picture'] : null;

        // Try to find existing mapping
        $stmt = $pdo->prepare('SELECT student_id FROM oauth_user WHERE provider = ? AND provider_user_id = ?');
        $stmt->execute([$provider, $providerUserId]);
        $row = $stmt->fetch();

        if ($row) {
            $studentId = (int)$row['student_id'];
        } else {
            // Create student record
            $firstName = $displayName;
            $lastName = '';
            if (strpos($displayName, ' ') !== false) {
                $parts = preg_split('/\s+/', $displayName, 2);
                $firstName = $parts[0];
                $lastName = $parts[1];
            }
            $stmt = $pdo->prepare('INSERT INTO student (name, surname, photo_link) VALUES (?, ?, ?)');
            $stmt->execute([$firstName, $lastName, $picture]);
            $studentId = (int)$pdo->lastInsertId();

            // Create oauth mapping
            $stmt = $pdo->prepare('INSERT INTO oauth_user (provider, provider_user_id, student_id) VALUES (?, ?, ?)');
            $stmt->execute([$provider, $providerUserId, $studentId]);
        }
        // No explicit transaction used; relying on autocommit

        // Store user info in session
        $_SESSION['user'] = [
            'id' => $providerUserId,
            'student_id' => $studentId,
            'name' => $displayName,
            'email' => $email,
            'picture' => $picture
        ];
    } catch (Throwable $e) {
        http_response_code(500);
        if (defined('DEBUG_MODE') && DEBUG_MODE) {
            echo json_encode(['success' => false, 'error' => 'DB error: ' . $e->getMessage()]);
        } else {
            echo json_encode(['success' => false, 'error' => 'DB error']);
        }
        exit;
    }
    
    echo json_encode(['success' => true]);
} else {
    echo json_encode(['success' => false, 'error' => 'Token verification failed']);
}
?>
