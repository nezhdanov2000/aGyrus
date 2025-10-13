<?php
/**
 * Intent prediction API endpoint
 * Calls Python intent classifier and returns JSON response
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

// Get input
$input = json_decode(file_get_contents('php://input'), true);
$text = $input['text'] ?? '';

if (empty($text)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Text is required']);
    exit;
}

// Call Python script with cleared LD_LIBRARY_PATH to avoid LAMPP lib conflicts
$scriptPath = realpath(__DIR__ . '/../core/intent_classifier.py');
$escapedText = escapeshellarg($text);
$command = "LD_LIBRARY_PATH= /usr/bin/python3 $scriptPath $escapedText 2>&1";

exec($command, $output, $returnCode);

// Parse output
if ($returnCode !== 0) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Failed to classify intent',
        'details' => implode("\n", $output)
    ]);
    exit;
}

// Extract intent and confidence from output
$intent = 'general';
$confidence = 0.0;

foreach ($output as $line) {
    if (strpos($line, 'Intent:') !== false) {
        $parts = explode(':', $line, 2);
        $intentPart = trim($parts[1]);
        $intent = explode(' ', $intentPart)[0];
    }
    if (strpos($line, 'Confidence:') !== false) {
        $parts = explode(':', $line, 2);
        $confidencePart = trim($parts[1]);
        $confidence = floatval(str_replace('%', '', $confidencePart)) / 100;
    }
}

echo json_encode([
    'success' => true,
    'intent' => $intent,
    'confidence' => $confidence,
    'text' => $text
]);

