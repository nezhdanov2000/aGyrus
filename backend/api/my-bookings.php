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

$studentId = $_SESSION['user']['student_id'];

try {
    $pdo = getPDO();
    
    // Get user's bookings (only active bookings exist in DB)
    $stmt = $pdo->prepare("
        SELECT b.booking_id, b.booking_date,
               t.tutor_id, t.date, bt.start_time, bt.end_time,
               tu.name as tutor_name, tu.surname as tutor_surname,
               c.course_name
        FROM booking b
        JOIN timeslot t ON b.timeslot_id = t.timeslot_id
        JOIN base_timeslot bt ON t.base_timeslot_id = bt.base_timeslot_id
        JOIN tutor tu ON t.tutor_id = tu.tutor_id
        JOIN course c ON b.course_id = c.course_id
        WHERE b.student_id = ?
        ORDER BY t.date, bt.start_time
    ");
    
    $stmt->execute([$studentId]);
    $bookings = $stmt->fetchAll();
    
    echo json_encode([
        'success' => true,
        'bookings' => $bookings
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
