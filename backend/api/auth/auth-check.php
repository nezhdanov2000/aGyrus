<?php
/**
 * Common authentication check for API endpoints
 * Include this file to check if user is authenticated
 */

if (!isset($_SESSION['user']) || !isset($_SESSION['user']['student_id'])) {
    http_response_code(401);
    echo json_encode([
        'success' => false,
        'error' => 'Not authenticated'
    ]);
    exit;
}
?>
