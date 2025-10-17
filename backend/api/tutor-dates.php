<?php
require_once '../config/config.php';

header('Content-Type: application/json');

// Check if user is logged in
if (!isset($_SESSION['user']) || !isset($_SESSION['user']['student_id'])) {
    http_response_code(401);
    echo json_encode(['success' => false, 'error' => 'Not authenticated']);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

$tutorId = (int)($_GET['tutor_id'] ?? 0);

if ($tutorId <= 0) {
    echo json_encode(['success' => false, 'error' => 'Valid tutor_id is required']);
    exit;
}

try {
    $pdo = getPDO();
    
    // Get available dates for tutor
    $stmt = $pdo->prepare("
        SELECT DISTINCT bt.date, 
               COUNT(t.timeslot_id) as available_slots
        FROM timeslot t
        JOIN base_timeslot bt ON t.base_timeslot_id = bt.base_timeslot_id
        WHERE t.tutor_id = ? 
        AND t.status = 'available' 
        AND bt.date >= CURDATE()
        GROUP BY bt.date
        ORDER BY bt.date
    ");
    
    $stmt->execute([$tutorId]);
    $dates = $stmt->fetchAll();
    
    echo json_encode([
        'success' => true,
        'dates' => $dates,
        'tutor_id' => $tutorId
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
