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
    telegram_id INT,
    description TEXT,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    photo_link VARCHAR(255)
);

CREATE TABLE student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    nickname VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE base_timeslot (
    base_timeslot_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    UNIQUE KEY unique_time_slot (date, start_time, end_time)
);

CREATE TABLE timeslot (
    timeslot_id INT AUTO_INCREMENT PRIMARY KEY,
    base_timeslot_id INT,
    tutor_id INT,
    course_id INT, 
    status ENUM('available', 'booked') DEFAULT 'available', 
    repeatability ENUM('single', 'repeated') DEFAULT 'single', 
    FOREIGN KEY (base_timeslot_id) REFERENCES base_timeslot(base_timeslot_id),
    FOREIGN KEY (tutor_id) REFERENCES tutor(tutor_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    UNIQUE KEY unique_tutor_timeslot (tutor_id, base_timeslot_id)
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

-- Seed data

-- Courses
INSERT INTO course (course_name) VALUES
    ('Mathematics'),
    ('Physics'),
    ('Computer Science');

-- Tutors
INSERT INTO tutor (telegram_id, description, name, surname, photo_link) VALUES
    (1001, 'Expert in calculus and algebra', 'Alice', 'Johnson', NULL),
    (1002, 'Physics PhD, mechanics and optics', 'Bob', 'Smith', NULL);

-- Students (with hashed passwords)
INSERT INTO student (nickname, email, password) VALUES
    ('student1', 'student1@example.com', '$2y$10$TKh8H1.PfQx37YgCzwiKb.KjNyWgaHb9cbcoQgdIVFlYg7B77UdFm'), -- password: pass1
    ('student2', 'student2@example.com', '$2y$10$TKh8H1.PfQx37YgCzwiKb.KjNyWgaHb9cbcoQgdIVFlYg7B77UdFm'); -- password: pass2

-- Base timeslots
-- 2025-10-20 is Monday
INSERT INTO base_timeslot (date, day_of_week, start_time, end_time) VALUES
    ('2025-10-20', 'Monday', '10:00:00', '11:00:00'),
    ('2025-10-20', 'Monday', '11:00:00', '12:00:00'),
    ('2025-10-21', 'Tuesday', '10:00:00', '11:00:00');

-- Tutor-course mapping
INSERT INTO tutor_course (tutor_id, course_id) VALUES
    (1, 1), -- Alice teaches Mathematics
    (1, 3), -- Alice teaches CS
    (2, 2); -- Bob teaches Physics

-- Timeslots (linking tutors and courses to base slots)
INSERT INTO timeslot (base_timeslot_id, tutor_id, course_id, status, repeatability) VALUES
    (1, 1, 1, 'available', 'single'),
    (2, 1, 3, 'booked', 'single'),
    (3, 2, 2, 'available', 'single');

-- Bookings (only for the booked timeslot above)
INSERT INTO booking (student_id, timeslot_id) VALUES
    (1, 2);
