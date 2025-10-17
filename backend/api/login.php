<?php
require_once '../config/config.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
$email = trim($input['email'] ?? '');
$password = trim($input['password'] ?? '');

if (empty($email) || empty($password)) {
    echo json_encode(['success' => false, 'error' => 'Email and password are required']);
    exit;
}

try {
    $pdo = getPDO();
    
    // Find student by email
    $stmt = $pdo->prepare("
        SELECT student_id, nickname, email, password 
        FROM student 
        WHERE email = ?
    ");
    $stmt->execute([$email]);
    $student = $stmt->fetch();
    
    if (!$student) {
        echo json_encode(['success' => false, 'error' => 'Invalid email or password']);
        exit;
    }
    
    // Verify password: support hashed (recommended) and legacy plaintext (auto-upgrade)
    $stored = $student['password'];
    $isValid = false;
    if (password_get_info($stored)['algo']) {
        // Stored value looks like a password_hash
        $isValid = password_verify($password, $stored);
    } else {
        // Legacy plaintext comparison
        $isValid = hash_equals($stored, $password);
        if ($isValid) {
            // Auto-upgrade to hashed password
            try {
                $newHash = password_hash($password, PASSWORD_DEFAULT);
                $up = $pdo->prepare("UPDATE student SET password = ? WHERE student_id = ?");
                $up->execute([$newHash, $student['student_id']]);
                $stored = $newHash;
            } catch (Throwable $e) {
                // Ignore upgrade failure; proceed with login since credentials matched
            }
        }
    }
    if (!$isValid) {
        echo json_encode(['success' => false, 'error' => 'Invalid email or password']);
        exit;
    }
    
    // Set session
    $_SESSION['user'] = [
        'student_id' => $student['student_id'],
        'nickname' => $student['nickname'],
        'email' => $student['email']
    ];
    
    echo json_encode([
        'success' => true,
        'user' => $_SESSION['user'],
        'message' => 'Login successful'
    ]);
    
} catch (Throwable $e) {
    http_response_code(500);
    if (defined('DEBUG_MODE') && DEBUG_MODE) {
        echo json_encode(['success' => false, 'error' => 'DB error: ' . $e->getMessage()]);
    } else {
        echo json_encode(['success' => false, 'error' => 'Database error']);
    }
}
?>
