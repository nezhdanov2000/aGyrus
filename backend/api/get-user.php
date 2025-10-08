<?php
require_once '../config/config.php';

// Ensure API returns clean JSON
header('Content-Type: application/json');

// Check if user is logged in
if (!isset($_SESSION['user'])) {
    echo json_encode([
        'success' => false,
        'error' => 'Not authenticated'
    ]);
    exit;
}

// Return user data
echo json_encode([
    'success' => true,
    'user' => $_SESSION['user']
]);
?>
