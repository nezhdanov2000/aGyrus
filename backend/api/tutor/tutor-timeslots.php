<?php
require_once '../../config/config.php';
require_once '../auth/auth-check.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

$tutorId = (int)($_GET['tutor_id'] ?? 0);
$date = $_GET['date'] ?? '';

if ($tutorId <= 0 || empty($date)) {
    echo json_encode(['success' => false, 'error' => 'Valid tutor_id and date are required']);
    exit;
}

// Validate date format
if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $date)) {
    echo json_encode(['success' => false, 'error' => 'Invalid date format']);
    exit;
}

try {
    $pdo = getPDO();
    
    // Get available timeslots for specific date
    $stmt = $pdo->prepare("
        SELECT t.timeslot_id, bt.date, bt.start_time, bt.end_time, bt.day_of_week
        FROM timeslot t
        JOIN base_timeslot bt ON t.base_timeslot_id = bt.base_timeslot_id
        WHERE t.tutor_id = ? 
        AND bt.date = ? 
        AND t.status = 'available'
        ORDER BY bt.start_time
    ");
    
    $stmt->execute([$tutorId, $date]);
    $timeslots = $stmt->fetchAll();
    
    echo json_encode([
        'success' => true,
        'timeslots' => $timeslots,
        'tutor_id' => $tutorId,
        'date' => $date
    ]);
    
} catch (Throwable $e) {
    http_response_code(500);
    if (defined('DEBUG_MODE') && DEBUG_MODE) {
        echo json_encode(['success' => false, 'error' => 'DB error: ' . $e->getMessage()]);
    } else {
        echo json_encode(['success' => false, 'error' => 'Database error']);
    }
}
?>
