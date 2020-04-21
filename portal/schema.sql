-- TSCT Portal Database Schema
--
-- This file will drop and recreate all tables necessary for
-- the application and can be run with the `flask init-db`
-- command in your terminal.

-- Drop existing tables
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS majors CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS roster CASCADE;
DROP TABLE IF EXISTS assignments CASCADE;

-- Users
CREATE TABLE users (
    id bigint PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password bytea NOT NULL,
    name text,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student')),
    major varchar(10)
);

CREATE TABLE majors (
  major_id bigserial PRIMARY KEY,
  name varchar(50) UNIQUE NOT NULL,
  description text
);

CREATE TABLE courses (
  course_id bigserial PRIMARY KEY,
  name varchar(50) UNIQUE NOT NULL,
  major varchar(50) NOT NULL,
  description text,
  credits int,
  teacherid bigint NOT NULL
);

ALTER TABLE courses
  ADD CONSTRAINT major_course FOREIGN KEY (major)
    REFERENCES majors(name)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE courses
  ADD CONSTRAINT course_teacher FOREIGN KEY (teacherid)
    REFERENCES users(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

CREATE TABLE sessions (
  id bigserial PRIMARY KEY,
  course_id bigint NOT NULL,
  days varchar(20) NOT NULL,
  class_time time NOT NULL,
  location varchar(50)
);

ALTER TABLE sessions
  ADD CONSTRAINT session_course_name FOREIGN KEY (course_id)
    REFERENCES courses(course_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

CREATE TABLE roster (
  count bigserial PRIMARY KEY,
  student_id bigint,
  session_id bigint
);

ALTER TABLE roster
  ADD CONSTRAINT student_id FOREIGN KEY (student_id)
    REFERENCES users(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE roster
  ADD CONSTRAINT session_id FOREIGN KEY (session_id)
    REFERENCES sessions(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

CREATE TABLE assignments(
  assignment_id bigserial PRIMARY KEY,
  session_id bigserial REFERENCES sessions(id),
  name text,
  description text,
  due_date date
);

INSERT INTO majors (name, description)
  VALUES ('ARCH', 'Architectural Technology'),
          ('AUTO', 'Automotive Technology'),
          ('BUSA', 'Buisiness Administration'),
          ('CSET', 'Computer Software Engineering Technology'),
          ('CARP', 'Carpentry Technology'),
          ('CNSA', 'Computer and Network Systems Administration'),
          ('ELEC', 'Electrical Technology'),
          ('MSON', 'Masonry Technology'),
          ('WELD', 'Welding Technology'),
          ('GEND', 'General Education');
