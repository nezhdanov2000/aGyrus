<?php
require_once '../config/config.php';

header('Content-Type: application/json');

// Check if user is logged in
if (!isset($_SESSION['user']) || !isset($_SESSION['user']['student_id'])) {
    http_response_code(401);
    echo json_encode(['success' => false, 'error' => 'Not authenticated']);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
$timeslotId = (int)($input['timeslot_id'] ?? 0);

if ($timeslotId <= 0) {
    echo json_encode(['success' => false, 'error' => 'Valid timeslot_id is required']);
    exit;
}

$studentId = $_SESSION['user']['student_id'];

try {
    $pdo = getPDO();
    
    // Check if timeslot is still available
    $stmt = $pdo->prepare("
        SELECT t.timeslot_id, t.status, t.tutor_id, bt.start_time, bt.end_time, bt.date
        FROM timeslot t
        JOIN base_timeslot bt ON t.base_timeslot_id = bt.base_timeslot_id
        WHERE t.timeslot_id = ? AND t.status = 'available'
    ");
    $stmt->execute([$timeslotId]);
    $timeslot = $stmt->fetch();
    
    if (!$timeslot) {
        echo json_encode(['success' => false, 'error' => 'Timeslot is no longer available']);
        exit;
    }
    
    // Check if student already has a booking for this timeslot
    $stmt = $pdo->prepare("
        SELECT booking_id FROM booking 
        WHERE student_id = ? AND timeslot_id = ?
    ");
    $stmt->execute([$studentId, $timeslotId]);
    if ($stmt->fetch()) {
        echo json_encode(['success' => false, 'error' => 'You already have a booking for this timeslot']);
        exit;
    }
    
    // Create booking
    $stmt = $pdo->prepare("
        INSERT INTO booking (student_id, timeslot_id) 
        VALUES (?, ?)
    ");
    $stmt->execute([$studentId, $timeslotId]);
    $bookingId = $pdo->lastInsertId();
    
    // Update timeslot status to booked
    $stmt = $pdo->prepare("
        UPDATE timeslot SET status = 'booked' WHERE timeslot_id = ?
    ");
    $stmt->execute([$timeslotId]);
    
    echo json_encode([
        'success' => true,
        'booking_id' => $bookingId,
        'message' => 'Booking created successfully'
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
