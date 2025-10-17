<?php
require_once '../../config/config.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
$newTimeslotId = (int)($input['timeslot_id'] ?? 0);

if ($newTimeslotId <= 0) {
    echo json_encode(['success' => false, 'error' => 'Valid timeslot_id is required']);
    exit;
}

try {
    $pdo = getPDO();
    
    // Get details of the new timeslot
    $stmt = $pdo->prepare("
        SELECT t.timeslot_id, t.tutor_id, t.course_id, t.status,
               bt.start_time, bt.end_time, bt.date, bt.day_of_week
        FROM timeslot t
        JOIN base_timeslot bt ON t.base_timeslot_id = bt.base_timeslot_id
        WHERE t.timeslot_id = ?
    ");
    $stmt->execute([$newTimeslotId]);
    $newTimeslot = $stmt->fetch();
    
    if (!$newTimeslot || $newTimeslot['status'] !== 'available') {
        echo json_encode(['success' => false, 'error' => 'Timeslot not found or not available']);
        exit;
    }
    
    // Find students with recurring bookings that match this pattern
    $stmt = $pdo->prepare("
        SELECT DISTINCT b.student_id, s.nickname
        FROM booking b
        JOIN timeslot t ON b.timeslot_id = t.timeslot_id
        JOIN base_timeslot bt ON t.base_timeslot_id = bt.base_timeslot_id
        JOIN student s ON b.student_id = s.student_id
        WHERE t.repeatability = 'repeated'
        AND t.tutor_id = ?
        AND t.course_id = ?
        AND bt.day_of_week = ?
        AND bt.start_time = ?
        AND bt.end_time = ?
        AND b.student_id NOT IN (
            SELECT student_id FROM booking 
            WHERE timeslot_id = ?
        )
    ");
    
    $stmt->execute([
        $newTimeslot['tutor_id'],
        $newTimeslot['course_id'],
        $newTimeslot['day_of_week'],
        $newTimeslot['start_time'],
        $newTimeslot['end_time'],
        $newTimeslotId
    ]);
    
    $matchingStudents = $stmt->fetchAll();
    $autoBookings = [];
    
    // Create automatic bookings for matching students
    foreach ($matchingStudents as $student) {
        try {
            // Create booking
            $stmt = $pdo->prepare("
                INSERT INTO booking (student_id, timeslot_id) 
                VALUES (?, ?)
            ");
            $stmt->execute([$student['student_id'], $newTimeslotId]);
            $bookingId = $pdo->lastInsertId();
            
            // Update timeslot status to booked and set as recurring
            $stmt = $pdo->prepare("
                UPDATE timeslot SET status = 'booked', repeatability = 'repeated' WHERE timeslot_id = ?
            ");
            $stmt->execute([$newTimeslotId]);
            
            $autoBookings[] = [
                'student_id' => $student['student_id'],
                'student_nickname' => $student['nickname'],
                'booking_id' => $bookingId
            ];
            
        } catch (Throwable $e) {
            // Log error but continue with other students
            error_log("Auto-booking failed for student {$student['student_id']}: " . $e->getMessage());
        }
    }
    
    echo json_encode([
        'success' => true,
        'auto_bookings' => $autoBookings,
        'count' => count($autoBookings),
        'message' => count($autoBookings) > 0 ? 
            'Automatic bookings created for ' . count($autoBookings) . ' students' :
            'No matching recurring bookings found'
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
