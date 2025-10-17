<?php
require_once '../../config/config.php';

// Decide response mode: redirect by default for browser GET; JSON when explicitly requested
$isGet = ($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'GET';
$wantsJson = isset($_GET['json']) || (isset($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest');

// Clear session
session_destroy();

if ($isGet && !$wantsJson) {
    // Redirect to login page
    header('Location: ../../frontend/html/index.html');
    exit;
}

header('Content-Type: application/json');
echo json_encode([
    'success' => true,
    'message' => 'Logged out successfully'
]);
?>
