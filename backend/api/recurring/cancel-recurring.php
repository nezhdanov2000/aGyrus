<?php
require_once '../../config/config.php';
require_once '../auth/auth-check.php';

header('Content-Type: application/json');

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
    
    // Get the timeslot details to find matching recurring bookings
    $stmt = $pdo->prepare("
        SELECT t.timeslot_id, t.tutor_id, t.course_id, t.repeatability,
               bt.start_time, bt.end_time, bt.day_of_week
        FROM timeslot t
        JOIN base_timeslot bt ON t.base_timeslot_id = bt.base_timeslot_id
        WHERE t.timeslot_id = ?
    ");
    $stmt->execute([$timeslotId]);
    $timeslot = $stmt->fetch();
    
    if (!$timeslot) {
        echo json_encode(['success' => false, 'error' => 'Timeslot not found']);
        exit;
    }
    
    if ($timeslot['repeatability'] !== 'repeated') {
        echo json_encode(['success' => false, 'error' => 'This is not a recurring booking']);
        exit;
    }
    
    // Find all future recurring bookings for this student with same pattern
    $stmt = $pdo->prepare("
        SELECT b.booking_id, b.timeslot_id, bt.date
        FROM booking b
        JOIN timeslot t ON b.timeslot_id = t.timeslot_id
        JOIN base_timeslot bt ON t.base_timeslot_id = bt.base_timeslot_id
        WHERE b.student_id = ?
        AND t.repeatability = 'repeated'
        AND t.tutor_id = ?
        AND t.course_id = ?
        AND bt.day_of_week = ?
        AND bt.start_time = ?
        AND bt.end_time = ?
        AND bt.date >= CURDATE()
        ORDER BY bt.date
    ");
    
    $stmt->execute([
        $studentId,
        $timeslot['tutor_id'],
        $timeslot['course_id'],
        $timeslot['day_of_week'],
        $timeslot['start_time'],
        $timeslot['end_time']
    ]);
    
    $recurringBookings = $stmt->fetchAll();
    
    if (empty($recurringBookings)) {
        echo json_encode(['success' => false, 'error' => 'No recurring bookings found']);
        exit;
    }
    
    $cancelledCount = 0;
    $cancelledDates = [];
    
    // Cancel all future recurring bookings
    foreach ($recurringBookings as $booking) {
        try {
            // Delete booking
            $stmt = $pdo->prepare("DELETE FROM booking WHERE booking_id = ?");
            $stmt->execute([$booking['booking_id']]);
            
            // Make timeslot available again
            $stmt = $pdo->prepare("UPDATE timeslot SET status = 'available' WHERE timeslot_id = ?");
            $stmt->execute([$booking['timeslot_id']]);
            
            $cancelledCount++;
            $cancelledDates[] = $booking['date'];
            
        } catch (Throwable $e) {
            error_log("Failed to cancel recurring booking {$booking['booking_id']}: " . $e->getMessage());
        }
    }
    
    echo json_encode([
        'success' => true,
        'cancelled_count' => $cancelledCount,
        'cancelled_dates' => $cancelledDates,
        'message' => "Cancelled {$cancelledCount} recurring bookings"
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
