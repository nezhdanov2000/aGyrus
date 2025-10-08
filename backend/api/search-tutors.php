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
$query = trim($input['query'] ?? '');

if (empty($query)) {
    echo json_encode(['success' => false, 'error' => 'Query is required']);
    exit;
}

try {
    $pdo = getPDO();
    
    // Search tutors by name, surname, or course
    $stmt = $pdo->prepare("
        SELECT DISTINCT t.tutor_id, t.name, t.surname, t.photo_link,
               GROUP_CONCAT(c.course_name SEPARATOR ', ') as courses,
               GROUP_CONCAT(c.course_id SEPARATOR ',') as course_ids
        FROM tutor t
        LEFT JOIN tutor_course tc ON t.tutor_id = tc.tutor_id
        LEFT JOIN course c ON tc.course_id = c.course_id
        WHERE t.name LIKE ? OR t.surname LIKE ? OR c.course_name LIKE ?
        GROUP BY t.tutor_id, t.name, t.surname, t.photo_link
        ORDER BY t.name, t.surname
    ");
    
    $searchTerm = "%{$query}%";
    $stmt->execute([$searchTerm, $searchTerm, $searchTerm]);
    $tutors = $stmt->fetchAll();
    
    echo json_encode([
        'success' => true,
        'tutors' => $tutors,
        'count' => count($tutors)
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
