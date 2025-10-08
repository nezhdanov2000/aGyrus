<?php
require_once '../config/config.php';

// Generate state parameter for security
$state = bin2hex(random_bytes(16));
$_SESSION['oauth_state'] = $state;

// Google OAuth URL with additional parameters for secure browsers
$authUrl = 'https://accounts.google.com/o/oauth2/auth?' . http_build_query([
    'client_id' => GOOGLE_CLIENT_ID,
    'redirect_uri' => GOOGLE_REDIRECT_URI,
    'scope' => 'email profile',
    'response_type' => 'code',
    'state' => $state,
    'access_type' => 'offline',
    'prompt' => 'select_account',
    'include_granted_scopes' => 'true'
]);

// Redirect to Google
header('Location: ' . $authUrl);
exit;
?>
