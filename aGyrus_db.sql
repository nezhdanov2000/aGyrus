DROP DATABASE IF EXISTS aGyrus_db;

-- Creating the database
CREATE DATABASE aGyrus_db;

-- Selecting the database to use
USE aGyrus_db;

-- Creating tables in correct order
CREATE TABLE course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL
);

CREATE TABLE tutor (
    tutor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    photo_link VARCHAR(255)
);

CREATE TABLE student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    photo_link VARCHAR(255)
);

CREATE TABLE base_timeslot (
    base_timeslot_id INT AUTO_INCREMENT PRIMARY KEY,
    day_of_week VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    UNIQUE KEY unique_time_slot (day_of_week, start_time, end_time)
);

CREATE TABLE timeslot (
    timeslot_id INT AUTO_INCREMENT PRIMARY KEY,
    base_timeslot_id INT,
    tutor_id INT,
    course_id INT, 
    date DATE NOT NULL,
    status ENUM('available', 'booked') DEFAULT 'available', 
    FOREIGN KEY (base_timeslot_id) REFERENCES base_timeslot(base_timeslot_id),
    FOREIGN KEY (tutor_id) REFERENCES tutor(tutor_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    UNIQUE KEY unique_tutor_timeslot (tutor_id, date, base_timeslot_id)
);

CREATE TABLE tutor_course (
    tutor_id INT,
    course_id INT,
    PRIMARY KEY (tutor_id, course_id),
    FOREIGN KEY (tutor_id) REFERENCES tutor(tutor_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE booking (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    timeslot_id INT,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (timeslot_id) REFERENCES timeslot(timeslot_id),
    UNIQUE KEY unique_student_timeslot (student_id, timeslot_id)
);

-- Seed data --------------------------------------------------

-- Courses
INSERT INTO course (course_name) VALUES
('Mathematics'),
('Physics'),
('Chemistry'),
('Biology'),
('Computer Science');

-- Tutors
INSERT INTO tutor (name, surname, photo_link) VALUES
('Walter', 'Whitman', 'https://picsum.photos/seed/t1/200'),
('Emily', 'Dickinson', 'https://picsum.photos/seed/t2/200'),
('Ada', 'Lovelace', 'https://picsum.photos/seed/t3/200');

-- Students
INSERT INTO student (name, surname, photo_link) VALUES
('John', 'Doe', 'https://picsum.photos/seed/s1/200'),
('Jane', 'Smith', 'https://picsum.photos/seed/s2/200'),
('Alex', 'Johnson', 'https://picsum.photos/seed/s3/200');

-- Base timeslots (weekday names as in current schema)
INSERT INTO base_timeslot (day_of_week, start_time, end_time) VALUES
('Monday', '09:00:00', '10:00:00'),
('Monday', '10:00:00', '11:00:00'),
('Tuesday', '14:00:00', '15:00:00'),
('Wednesday', '09:00:00', '10:00:00'),
('Friday', '16:00:00', '17:00:00');

-- Tutor-course relations
-- Walter: Math, Physics; Emily: Biology; Ada: Computer Science, Math
INSERT INTO tutor_course (tutor_id, course_id) VALUES
(1, 1), (1, 2),
(2, 4),
(3, 5), (3, 1);

-- Timeslots sample data
INSERT INTO timeslot (base_timeslot_id, tutor_id, course_id, date, status) VALUES
-- Walter: занятия на 3 октября 2025
(1, 1, 1, '2025-10-03', 'available'),  -- Walter: Math (09:00-10:00)
(2, 1, 1, '2025-10-03', 'available'),  -- Walter: Math (10:00-11:00)
(3, 1, 1, '2025-10-03', 'available'),  -- Walter: Math (14:00-15:00)
(4, 1, 1, '2025-10-03', 'available'),  -- Walter: Math (09:00-10:00)
(5, 1, 1, '2025-10-03', 'available'),  -- Walter: Math (16:00-17:00)
-- Walter: Multiple Math sessions (будущие даты)
(1, 1, 1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Walter: Math (09:00)
(2, 1, 1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Walter: Math (10:00)
(3, 1, 1, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Walter: Math (14:00)
(4, 1, 1, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'),  -- Walter: Math (09:00)
(5, 1, 1, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'),  -- Walter: Math (16:00)
-- Other tutors
(3, 2, 4, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Emily: Biology
(4, 3, 5, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Ada: Computer Science
(5, 3, 1, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'); -- Ada: Math

