<?php
require_once '../../config/config.php';

// Check if state parameter matches
if (!isset($_GET['state']) || $_GET['state'] !== $_SESSION['oauth_state']) {
    die('Invalid state parameter');
}

// Check for authorization code
if (!isset($_GET['code'])) {
    die('Authorization code not found');
}

$code = $_GET['code'];

// Exchange code for access token
$tokenUrl = 'https://oauth2.googleapis.com/token';
$tokenData = [
    'client_id' => GOOGLE_CLIENT_ID,
    'client_secret' => GOOGLE_CLIENT_SECRET,
    'redirect_uri' => GOOGLE_REDIRECT_URI,
    'grant_type' => 'authorization_code',
    'code' => $code
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $tokenUrl);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($tokenData));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/x-www-form-urlencoded']);

$response = curl_exec($ch);
curl_close($ch);

$tokenData = json_decode($response, true);

if (isset($tokenData['access_token'])) {
    // Get user info
    $userInfoUrl = 'https://www.googleapis.com/oauth2/v2/userinfo?access_token=' . $tokenData['access_token'];
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $userInfoUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    
    $userResponse = curl_exec($ch);
    curl_close($ch);
    
    $userInfo = json_decode($userResponse, true);
    
    // Store user info in session
    $_SESSION['user'] = [
        'id' => $userInfo['id'],
        'name' => $userInfo['name'],
        'email' => $userInfo['email'],
        'picture' => $userInfo['picture']
    ];
    
    // Redirect to chatbot landing after authentication
    header('Location: /frontend/html/chat.html');
    exit;
} else {
    die('Failed to get access token');
}
?>
