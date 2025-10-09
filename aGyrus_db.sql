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
('Ada', 'Lovelace', 'https://picsum.photos/seed/t3/200'),
('Isaac', 'Newton', 'https://picsum.photos/seed/t4/200'),
('Marie', 'Curie', 'https://picsum.photos/seed/t5/200'),
('Albert', 'Einstein', 'https://picsum.photos/seed/t6/200'),
('Charles', 'Darwin', 'https://picsum.photos/seed/t7/200'),
('Grace', 'Hopper', 'https://picsum.photos/seed/t8/200');

-- Students
INSERT INTO student (name, surname, photo_link) VALUES
('John', 'Doe', 'https://picsum.photos/seed/s1/200'),
('Jane', 'Smith', 'https://picsum.photos/seed/s2/200'),
('Alex', 'Johnson', 'https://picsum.photos/seed/s3/200');

-- Base timeslots (weekday names as in current schema)
INSERT INTO base_timeslot (day_of_week, start_time, end_time) VALUES
('Monday', '09:00:00', '10:00:00'),
('Monday', '10:00:00', '11:00:00'),
('Monday', '11:00:00', '12:00:00'),
('Monday', '14:00:00', '15:00:00'),
('Monday', '15:00:00', '16:00:00'),
('Tuesday', '09:00:00', '10:00:00'),
('Tuesday', '10:00:00', '11:00:00'),
('Tuesday', '14:00:00', '15:00:00'),
('Tuesday', '15:00:00', '16:00:00'),
('Tuesday', '16:00:00', '17:00:00'),
('Wednesday', '09:00:00', '10:00:00'),
('Wednesday', '10:00:00', '11:00:00'),
('Wednesday', '11:00:00', '12:00:00'),
('Wednesday', '14:00:00', '15:00:00'),
('Thursday', '09:00:00', '10:00:00'),
('Thursday', '10:00:00', '11:00:00'),
('Thursday', '14:00:00', '15:00:00'),
('Thursday', '15:00:00', '16:00:00'),
('Friday', '09:00:00', '10:00:00'),
('Friday', '10:00:00', '11:00:00'),
('Friday', '14:00:00', '15:00:00'),
('Friday', '15:00:00', '16:00:00'),
('Friday', '16:00:00', '17:00:00');

-- Tutor-course relations
-- Walter: Math, Physics; Emily: Biology; Ada: Computer Science, Math
-- Isaac: Physics, Math; Marie: Chemistry, Physics; Albert: Physics, Math
-- Charles: Biology, Chemistry; Grace: Computer Science
INSERT INTO tutor_course (tutor_id, course_id) VALUES
(1, 1), (1, 2),
(2, 4),
(3, 5), (3, 1),
(4, 2), (4, 1),
(5, 3), (5, 2),
(6, 2), (6, 1),
(7, 4), (7, 3),
(8, 5);

-- Timeslots sample data
INSERT INTO timeslot (base_timeslot_id, tutor_id, course_id, date, status) VALUES
-- Walter Whitman (ID:1): Math and Physics - Week 1
(1, 1, 1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 09:00 Math
(4, 1, 2, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 14:00 Physics
(6, 1, 1, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 09:00 Math
(9, 1, 2, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 15:00 Physics
(11, 1, 1, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 09:00 Math
(14, 1, 2, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 14:00 Physics
(15, 1, 1, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 09:00 Math
(17, 1, 2, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 14:00 Physics
(19, 1, 1, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 09:00 Math
(21, 1, 2, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 14:00 Physics

-- Walter Whitman - Week 2
(1, 1, 1, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 09:00 Math
(4, 1, 2, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 14:00 Physics
(6, 1, 1, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 09:00 Math
(8, 1, 2, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 14:00 Physics
(11, 1, 1, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 09:00 Math
(13, 1, 2, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 11:00 Physics
(16, 1, 1, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 10:00 Math
(18, 1, 2, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 15:00 Physics
(19, 1, 1, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 09:00 Math
(22, 1, 2, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 15:00 Physics

-- Emily Dickinson (ID:2): Biology - Week 1
(2, 2, 4, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 10:00 Biology
(5, 2, 4, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 15:00 Biology
(7, 2, 4, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 10:00 Biology
(10, 2, 4, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'), -- Tuesday 16:00 Biology
(12, 2, 4, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 10:00 Biology
(16, 2, 4, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 10:00 Biology
(18, 2, 4, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 15:00 Biology
(20, 2, 4, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 10:00 Biology
(23, 2, 4, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 16:00 Biology

-- Emily Dickinson - Week 2
(2, 2, 4, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 10:00 Biology
(5, 2, 4, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 15:00 Biology
(7, 2, 4, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 10:00 Biology
(9, 2, 4, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 15:00 Biology
(11, 2, 4, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 09:00 Biology
(14, 2, 4, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 14:00 Biology
(15, 2, 4, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 09:00 Biology
(17, 2, 4, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 14:00 Biology
(20, 2, 4, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 10:00 Biology

-- Ada Lovelace (ID:3): Computer Science and Math - Week 1
(3, 3, 5, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 11:00 CS
(6, 3, 1, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 09:00 Math
(10, 3, 5, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'), -- Tuesday 16:00 CS
(13, 3, 1, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 11:00 Math
(15, 3, 5, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 09:00 CS
(18, 3, 1, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 15:00 Math
(21, 3, 5, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 14:00 CS
(23, 3, 1, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 16:00 Math

-- Ada Lovelace - Week 2
(1, 3, 5, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 09:00 CS
(5, 3, 1, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 15:00 Math
(6, 3, 5, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 09:00 CS
(10, 3, 1, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'), -- Tuesday 16:00 Math
(12, 3, 5, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 10:00 CS
(14, 3, 1, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 14:00 Math
(16, 3, 5, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 10:00 CS
(18, 3, 1, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 15:00 Math
(20, 3, 5, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 10:00 CS
(22, 3, 1, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 15:00 Math

-- Isaac Newton (ID:4): Physics and Math - Week 1
(2, 4, 2, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 10:00 Physics
(5, 4, 1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 15:00 Math
(8, 4, 2, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 14:00 Physics
(11, 4, 1, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 09:00 Math
(14, 4, 2, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 14:00 Physics
(16, 4, 1, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 10:00 Math
(17, 4, 2, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 14:00 Physics
(20, 4, 1, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 10:00 Math
(22, 4, 2, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 15:00 Physics

-- Isaac Newton - Week 2
(2, 4, 2, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 10:00 Physics
(4, 4, 1, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 14:00 Math
(7, 4, 2, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 10:00 Physics
(9, 4, 1, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 15:00 Math
(12, 4, 2, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 10:00 Physics
(13, 4, 1, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 11:00 Math
(15, 4, 2, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 09:00 Physics
(17, 4, 1, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 14:00 Math
(19, 4, 2, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 09:00 Physics
(21, 4, 1, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 14:00 Math

-- Marie Curie (ID:5): Chemistry and Physics - Week 1
(1, 5, 3, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 09:00 Chemistry
(3, 5, 2, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 11:00 Physics
(7, 5, 3, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 10:00 Chemistry
(9, 5, 2, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 15:00 Physics
(12, 5, 3, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 10:00 Chemistry
(15, 5, 2, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 09:00 Physics
(17, 5, 3, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 14:00 Chemistry
(19, 5, 2, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 09:00 Physics
(22, 5, 3, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 15:00 Chemistry

-- Marie Curie - Week 2
(1, 5, 3, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 09:00 Chemistry
(3, 5, 2, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 11:00 Physics
(6, 5, 3, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 09:00 Chemistry
(8, 5, 2, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 14:00 Physics
(11, 5, 3, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 09:00 Chemistry
(13, 5, 2, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 11:00 Physics
(15, 5, 3, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 09:00 Chemistry
(18, 5, 2, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 15:00 Physics
(19, 5, 3, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 09:00 Chemistry
(21, 5, 2, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 14:00 Physics

-- Albert Einstein (ID:6): Physics and Math - Week 1
(2, 6, 2, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'booked'),     -- Monday 10:00 Physics (BOOKED)
(4, 6, 1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 14:00 Math
(6, 6, 2, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 09:00 Physics
(8, 6, 1, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 14:00 Math
(11, 6, 2, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 09:00 Physics
(13, 6, 1, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 11:00 Math
(15, 6, 2, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 09:00 Physics
(18, 6, 1, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 15:00 Math
(20, 6, 2, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 10:00 Physics
(21, 6, 1, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 14:00 Math

-- Albert Einstein - Week 2
(2, 6, 2, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 10:00 Physics
(5, 6, 1, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 15:00 Math
(7, 6, 2, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 10:00 Physics
(10, 6, 1, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'), -- Tuesday 16:00 Math
(12, 6, 2, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 10:00 Physics
(14, 6, 1, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 14:00 Math
(16, 6, 2, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 10:00 Physics
(17, 6, 1, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 14:00 Math
(19, 6, 2, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 09:00 Physics
(23, 6, 1, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 16:00 Math

-- Charles Darwin (ID:7): Biology and Chemistry - Week 1
(3, 7, 4, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 11:00 Biology
(4, 7, 3, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 14:00 Chemistry
(8, 7, 4, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 14:00 Biology
(10, 7, 3, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'), -- Tuesday 16:00 Chemistry
(12, 7, 4, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 10:00 Biology
(13, 7, 3, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 11:00 Chemistry
(16, 7, 4, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 10:00 Biology
(17, 7, 3, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 14:00 Chemistry
(20, 7, 4, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 10:00 Biology
(23, 7, 3, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 16:00 Chemistry

-- Charles Darwin - Week 2
(3, 7, 4, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 11:00 Biology
(5, 7, 3, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 15:00 Chemistry
(8, 7, 4, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 14:00 Biology
(10, 7, 3, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'), -- Tuesday 16:00 Chemistry
(11, 7, 4, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 09:00 Biology
(13, 7, 3, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 11:00 Chemistry
(15, 7, 4, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 09:00 Biology
(18, 7, 3, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 15:00 Chemistry
(20, 7, 4, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 10:00 Biology
(22, 7, 3, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 15:00 Chemistry

-- Grace Hopper (ID:8): Computer Science - Week 1
(1, 8, 5, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 09:00 CS
(5, 8, 5, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'available'),  -- Monday 15:00 CS
(7, 8, 5, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 10:00 CS
(9, 8, 5, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'available'),  -- Tuesday 15:00 CS
(11, 8, 5, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 09:00 CS
(14, 8, 5, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'available'), -- Wednesday 14:00 CS
(15, 8, 5, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 09:00 CS
(18, 8, 5, DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'available'), -- Thursday 15:00 CS
(19, 8, 5, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 09:00 CS
(22, 8, 5, DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'available'), -- Friday 15:00 CS

-- Grace Hopper - Week 2
(2, 8, 5, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 10:00 CS
(4, 8, 5, DATE_ADD(CURDATE(), INTERVAL 8 DAY), 'available'),  -- Monday 14:00 CS
(6, 8, 5, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 09:00 CS
(9, 8, 5, DATE_ADD(CURDATE(), INTERVAL 9 DAY), 'available'),  -- Tuesday 15:00 CS
(12, 8, 5, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 10:00 CS
(14, 8, 5, DATE_ADD(CURDATE(), INTERVAL 10 DAY), 'available'), -- Wednesday 14:00 CS
(16, 8, 5, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 10:00 CS
(17, 8, 5, DATE_ADD(CURDATE(), INTERVAL 11 DAY), 'available'), -- Thursday 14:00 CS
(20, 8, 5, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'), -- Friday 10:00 CS
(23, 8, 5, DATE_ADD(CURDATE(), INTERVAL 12 DAY), 'available'); -- Friday 16:00 CS

