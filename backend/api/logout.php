<?php
require_once '../config/config.php';

// Clear session
session_destroy();

// Redirect to home page
header('Location: /frontend/html/');
exit;
?>
