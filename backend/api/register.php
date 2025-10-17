<?php
require_once '../config/config.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
$nickname = trim($input['username'] ?? '');
$email = trim($input['email'] ?? '');
$password = trim($input['password'] ?? '');
$confirmPassword = trim($input['confirmPassword'] ?? '');

// Validation
if (empty($nickname) || empty($email) || empty($password) || empty($confirmPassword)) {
    echo json_encode(['success' => false, 'error' => 'All fields are required']);
    exit;
}

if ($password !== $confirmPassword) {
    echo json_encode(['success' => false, 'error' => 'Passwords do not match']);
    exit;
}

if (strlen($password) < 6) {
    echo json_encode(['success' => false, 'error' => 'Password must be at least 6 characters long']);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['success' => false, 'error' => 'Invalid email format']);
    exit;
}

try {
    $pdo = getPDO();
    
    // Check if email already exists
    $stmt = $pdo->prepare("SELECT student_id FROM student WHERE email = ?");
    $stmt->execute([$email]);
    if ($stmt->fetch()) {
        echo json_encode(['success' => false, 'error' => 'Email already registered']);
        exit;
    }
    
    // Check if nickname already exists
    $stmt = $pdo->prepare("SELECT student_id FROM student WHERE nickname = ?");
    $stmt->execute([$nickname]);
    if ($stmt->fetch()) {
        echo json_encode(['success' => false, 'error' => 'Username already taken']);
        exit;
    }
    
    // Create new student with securely hashed password
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
    $stmt = $pdo->prepare("
        INSERT INTO student (nickname, email, password) 
        VALUES (?, ?, ?)
    ");
    $stmt->execute([$nickname, $email, $hashedPassword]);
    $studentId = $pdo->lastInsertId();
    
    // Set session
    $_SESSION['user'] = [
        'student_id' => $studentId,
        'nickname' => $nickname,
        'email' => $email
    ];
    
    echo json_encode([
        'success' => true,
        'user' => $_SESSION['user'],
        'message' => 'Registration successful'
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
