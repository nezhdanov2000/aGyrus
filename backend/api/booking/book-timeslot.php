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
$isRecurring = ($input['recurring'] ?? false) === true;

if ($timeslotId <= 0) {
    echo json_encode(['success' => false, 'error' => 'Valid timeslot_id is required']);
    exit;
}

$studentId = $_SESSION['user']['student_id'];

try {
    $pdo = getPDO();
    
    // Check if timeslot is still available and get details
    $stmt = $pdo->prepare("
        SELECT t.timeslot_id, t.status, t.tutor_id, t.course_id, t.repeatability,
               bt.start_time, bt.end_time, bt.date, bt.day_of_week
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
    
    // Update timeslot status to booked and set repeatability
    $newRepeatability = $isRecurring ? 'repeated' : 'single';
    $stmt = $pdo->prepare("
        UPDATE timeslot SET status = 'booked', repeatability = ? WHERE timeslot_id = ?
    ");
    $stmt->execute([$newRepeatability, $timeslotId]);
    
    $message = $isRecurring ? 
        'Recurring booking created successfully. You will be automatically booked for similar timeslots.' :
        'Booking created successfully';
    
    // If it's a recurring booking, also book existing matching timeslots
    $existingBookings = [];
    if ($isRecurring) {
        try {
            // Find and book existing matching timeslots
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
                $timeslot['tutor_id'],
                $timeslot['course_id'],
                $timeslot['day_of_week'],
                $timeslot['start_time'],
                $timeslot['end_time'],
                $timeslotId,
                $studentId
            ]);
            
            $availableTimeslots = $stmt->fetchAll();
            
            // Create automatic bookings for existing matching timeslots
            foreach ($availableTimeslots as $existingTimeslot) {
                try {
                    // Create booking
                    $stmt = $pdo->prepare("
                        INSERT INTO booking (student_id, timeslot_id) 
                        VALUES (?, ?)
                    ");
                    $stmt->execute([$studentId, $existingTimeslot['timeslot_id']]);
                    $existingBookingId = $pdo->lastInsertId();
                    
                    // Update timeslot status to booked and set as recurring
                    $stmt = $pdo->prepare("
                        UPDATE timeslot SET status = 'booked', repeatability = 'repeated' WHERE timeslot_id = ?
                    ");
                    $stmt->execute([$existingTimeslot['timeslot_id']]);
                    
                    $existingBookings[] = [
                        'timeslot_id' => $existingTimeslot['timeslot_id'],
                        'date' => $existingTimeslot['date'],
                        'booking_id' => $existingBookingId
                    ];
                    
                } catch (Throwable $e) {
                    error_log("Auto-booking existing timeslot failed: " . $e->getMessage());
                }
            }
            
        } catch (Throwable $e) {
            error_log("Failed to find existing matching timeslots: " . $e->getMessage());
        }
    }
    
    echo json_encode([
        'success' => true,
        'booking_id' => $bookingId,
        'recurring' => $isRecurring,
        'existing_bookings' => $existingBookings,
        'existing_count' => count($existingBookings),
        'message' => $isRecurring && count($existingBookings) > 0 ? 
            "Recurring booking created! Also booked {$existingBookings} existing matching timeslots." :
            $message
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
