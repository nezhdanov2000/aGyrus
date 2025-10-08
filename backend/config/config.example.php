<?php
/**
 * Configuration Example File
 * 
 * Copy this file to config.php and fill in your credentials
 * DO NOT commit config.php to version control
 */

// Google OAuth Configuration
define('GOOGLE_CLIENT_ID', 'your-google-client-id-here');
define('GOOGLE_CLIENT_SECRET', 'your-google-client-secret-here');
define('GOOGLE_REDIRECT_URI', 'http://localhost/backend/auth/google/callback.php');

// Session configuration
session_start();

// Database configuration (if needed in future)
// define('DB_HOST', 'localhost');
// define('DB_NAME', 'classtime');
// define('DB_USER', 'root');
// define('DB_PASS', '');

// Application settings
define('APP_NAME', 'ClassTime');
define('APP_URL', 'http://localhost');

// Debug mode (set to false in production)
define('DEBUG_MODE', true);

if (DEBUG_MODE) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}
?>
