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
$bookingId = (int)($input['booking_id'] ?? 0);

if ($bookingId <= 0) {
    echo json_encode(['success' => false, 'error' => 'Valid booking_id is required']);
    exit;
}

$studentId = $_SESSION['user']['student_id'];

try {
    $pdo = getPDO();
    
    // Check if booking belongs to user
    $stmt = $pdo->prepare("
        SELECT b.booking_id, b.timeslot_id
        FROM booking b
        WHERE b.booking_id = ? AND b.student_id = ?
    ");
    $stmt->execute([$bookingId, $studentId]);
    $booking = $stmt->fetch();
    
    if (!$booking) {
        echo json_encode(['success' => false, 'error' => 'Booking not found']);
        exit;
    }
    
    // Delete booking (no history of cancelled bookings)
    $stmt = $pdo->prepare("
        DELETE FROM booking WHERE booking_id = ?
    ");
    $stmt->execute([$bookingId]);
    
    // Make timeslot available again
    $stmt = $pdo->prepare("
        UPDATE timeslot SET status = 'available' WHERE timeslot_id = ?
    ");
    $stmt->execute([$booking['timeslot_id']]);
    
    echo json_encode([
        'success' => true,
        'message' => 'Booking cancelled successfully'
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
