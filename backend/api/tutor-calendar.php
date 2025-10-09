<?php
require_once '../config/config.php';

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { exit(0); }

try {
    $pdo = getPDO();

    $month = isset($_GET['month']) ? (int)$_GET['month'] : date('n');
    $year = isset($_GET['year']) ? (int)$_GET['year'] : date('Y');
    $tutorId = isset($_GET['tutor_id']) ? (int)$_GET['tutor_id'] : 0;

    if ($month < 1 || $month > 12) { throw new Exception('Invalid month'); }
    if ($year < 2020 || $year > 2030) { throw new Exception('Invalid year'); }

    $sql = "
        SELECT 
            t.timeslot_id,
            t.date,
            t.status,
            bt.day_of_week,
            bt.start_time,
            bt.end_time,
            tu.name as tutor_name,
            tu.surname as tutor_surname,
            c.course_name,
            b.booking_id,
            b.student_id,
            s.name as student_name,
            s.surname as student_surname
        FROM timeslot t
        JOIN base_timeslot bt ON t.base_timeslot_id = bt.base_timeslot_id
        JOIN tutor tu ON t.tutor_id = tu.tutor_id
        LEFT JOIN booking b ON t.timeslot_id = b.timeslot_id
        LEFT JOIN student s ON b.student_id = s.student_id
        LEFT JOIN course c ON t.course_id = c.course_id
        WHERE YEAR(t.date) = :year AND MONTH(t.date) = :month" . ($tutorId > 0 ? "\n        AND t.tutor_id = :tutor_id" : "") . "
        ORDER BY t.date, bt.start_time
    ";

    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':year', $year, PDO::PARAM_INT);
    $stmt->bindParam(':month', $month, PDO::PARAM_INT);
    if ($tutorId > 0) { $stmt->bindParam(':tutor_id', $tutorId, PDO::PARAM_INT); }
    $stmt->execute();

    $timeslots = $stmt->fetchAll(PDO::FETCH_ASSOC);
    $calendarData = [];
    foreach ($timeslots as $ts) {
        $date = $ts['date'];
        if (!isset($calendarData[$date])) { $calendarData[$date] = []; }
        $calendarData[$date][] = [
            'timeslot_id' => $ts['timeslot_id'],
            'start_time' => $ts['start_time'],
            'end_time' => $ts['end_time'],
            'status' => $ts['status'],
            'tutor_name' => $ts['tutor_name'] . ' ' . $ts['tutor_surname'],
            'course_name' => $ts['course_name'],
            'is_booked' => !empty($ts['booking_id']),
            'booking_id' => $ts['booking_id'],
            'student_id' => $ts['student_id'],
            'student_name' => $ts['student_name'] ? $ts['student_name'] . ' ' . $ts['student_surname'] : null
        ];
    }

    echo json_encode(['success'=>true,'month'=>$month,'year'=>$year,'data'=>$calendarData]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success'=>false,'error'=>$e->getMessage()]);
}
?>


