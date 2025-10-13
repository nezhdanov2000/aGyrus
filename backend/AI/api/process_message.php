<?php
/**
 * Main AI message processing endpoint
 * Handles natural language understanding and dialog management
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
$message = $input['message'] ?? '';
$context = $input['context'] ?? [];

if (empty($message)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Message is required']);
    exit;
}

// Call Python dialog manager
$scriptPath = realpath(__DIR__ . '/../core/dialog_manager.py');
$escapedMessage = escapeshellarg($message);

// Pass context as JSON if provided
$contextJson = !empty($context) ? escapeshellarg(json_encode($context)) : "'{}'";

// Clear LD_LIBRARY_PATH to avoid LAMPP lib conflicts
$command = "LD_LIBRARY_PATH= /usr/bin/python3 $scriptPath $escapedMessage $contextJson 2>&1";

exec($command, $output, $returnCode);

if ($returnCode !== 0) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Failed to process message',
        'details' => implode("\n", $output)
    ]);
    exit;
}

// Parse JSON output from Python
$outputText = implode("\n", $output);

// Find JSON in output (in case there's debug output)
$jsonStart = strpos($outputText, '{');
if ($jsonStart !== false) {
    $jsonText = substr($outputText, $jsonStart);
    $result = json_decode($jsonText, true);
    
    if ($result !== null) {
        // Add success flag
        $result['success'] = true;
        echo json_encode($result, JSON_UNESCAPED_UNICODE);
    } else {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'error' => 'Invalid JSON response from dialog manager',
            'output' => $outputText
        ]);
    }
} else {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'No JSON output from dialog manager',
        'output' => $outputText
    ]);
}

