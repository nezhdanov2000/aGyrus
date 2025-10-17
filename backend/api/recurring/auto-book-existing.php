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
    
    // Get details of the timeslot that student just booked
    $stmt = $pdo->prepare("
        SELECT t.timeslot_id, t.tutor_id, t.course_id, t.repeatability,
               bt.start_time, bt.end_time, bt.date, bt.day_of_week
        FROM timeslot t
        JOIN base_timeslot bt ON t.base_timeslot_id = bt.base_timeslot_id
        WHERE t.timeslot_id = ?
    ");
    $stmt->execute([$timeslotId]);
    $bookedTimeslot = $stmt->fetch();
    
    if (!$bookedTimeslot || $bookedTimeslot['repeatability'] !== 'repeated') {
        echo json_encode([
            'success' => true,
            'message' => 'Not a recurring booking or timeslot not found',
            'auto_bookings' => []
        ]);
        exit;
    }
    
    // Find ALL existing available timeslots that match this pattern
    $stmt = $pdo->prepare("
        SELECT t.timeslot_id, bt.date
        FROM timeslot t
        JOIN base_timeslot bt ON t.base_timeslot_id = bt.base_timeslot_id
        WHERE t.tutor_id = ?
        AND t.course_id = ?
        AND bt.day_of_week = ?
        AND bt.start_time = ?
        AND bt.end_time = ?
        AND t.status = 'available'
        AND bt.date >= CURDATE()
        AND t.timeslot_id != ?
        AND t.timeslot_id NOT IN (
            SELECT timeslot_id FROM booking WHERE student_id = ?
        )
        ORDER BY bt.date
    ");
    
    $stmt->execute([
        $bookedTimeslot['tutor_id'],
        $bookedTimeslot['course_id'],
        $bookedTimeslot['day_of_week'],
        $bookedTimeslot['start_time'],
        $bookedTimeslot['end_time'],
        $timeslotId,
        $studentId
    ]);
    
    $availableTimeslots = $stmt->fetchAll();
    $autoBookings = [];
    
    // Create automatic bookings for all matching available timeslots
    foreach ($availableTimeslots as $timeslot) {
        try {
            // Create booking
            $stmt = $pdo->prepare("
                INSERT INTO booking (student_id, timeslot_id) 
                VALUES (?, ?)
            ");
            $stmt->execute([$studentId, $timeslot['timeslot_id']]);
            $bookingId = $pdo->lastInsertId();
            
            // Update timeslot status to booked and set as recurring
            $stmt = $pdo->prepare("
                UPDATE timeslot SET status = 'booked', repeatability = 'repeated' WHERE timeslot_id = ?
            ");
            $stmt->execute([$timeslot['timeslot_id']]);
            
            $autoBookings[] = [
                'timeslot_id' => $timeslot['timeslot_id'],
                'date' => $timeslot['date'],
                'booking_id' => $bookingId
            ];
            
        } catch (Throwable $e) {
            // Log error but continue with other timeslots
            error_log("Auto-booking failed for timeslot {$timeslot['timeslot_id']}: " . $e->getMessage());
        }
    }
    
    echo json_encode([
        'success' => true,
        'auto_bookings' => $autoBookings,
        'count' => count($autoBookings),
        'message' => count($autoBookings) > 0 ? 
            'Automatically booked ' . count($autoBookings) . ' existing matching timeslots' :
            'No existing matching timeslots found'
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
