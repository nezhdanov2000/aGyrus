<?php
// Dynamic base URL detection
$protocol = isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? 'https' : 'http';
$host = $_SERVER['HTTP_HOST'];
$scriptDir = dirname($_SERVER['SCRIPT_NAME']);
$baseUrl = $protocol . '://' . $host;

// Google OAuth Configuration
define('GOOGLE_CLIENT_ID', '731314897697-cus8dmpsc44gsfsqteetbp4bu0vlpa9o.apps.googleusercontent.com');
define('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET');
// Dynamic redirect URI based on current server
define('GOOGLE_REDIRECT_URI', $baseUrl . '/backend/auth/google/callback.php');

// Session configuration
session_start();

// Database configuration (env overrides local defaults)
if (!defined('DB_HOST')) define('DB_HOST', getenv('DB_HOST') ?: '127.0.0.1');
if (!defined('DB_NAME')) define('DB_NAME', getenv('DB_NAME') ?: 'aGyrus_db');
if (!defined('DB_USER')) define('DB_USER', getenv('DB_USER') ?: 'root');
if (!defined('DB_PASS')) define('DB_PASS', getenv('DB_PASS') ?: 'mega55555');

// Debug mode (set to false in production)
if (!defined('DEBUG_MODE')) define('DEBUG_MODE', true); // set to false in prod
if (DEBUG_MODE) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
}

// PDO helper (singleton)
function getPDO() {
    static $pdo = null;
    if ($pdo instanceof PDO) {
        return $pdo;
    }
    $dsn = 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4';
    $options = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
    ];
    try {
        $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
    } catch (Throwable $e) {
        if (DEBUG_MODE) {
            error_log('DB connection failed: ' . $e->getMessage());
        }
        throw $e;
    }
    return $pdo;
}
?>
