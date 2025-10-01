CREATE DATABASE IF NOT EXISTS my_lab
DEFAULT CHARACTER SET utf8mb4;

USE my_lab;

DROP TABLE IF EXISTS teachers, papers, projects, courses, teacher_post_paper, teacher_hold_project, teacher_teach_course;

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id CHAR(5) PRIMARY KEY,
    teacher_name VARCHAR(256) NOT NULL,
    gender int,
    position int,
    password VARCHAR(256) NOT NULL
) CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS papers (
    paper_id int PRIMARY KEY,
    paper_name VARCHAR(256) NOT NULL,
    source VARCHAR(256),
    post_year int,
    paper_type int,
    level int
) CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS projects (
    project_id VARCHAR(256) PRIMARY KEY,
    project_name VARCHAR(256) NOT NULL,
    project_source VARCHAR(256),
    project_type int,
    project_money FLOAT,
    start_year int,
    end_year int
) CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS courses (
    course_id VARCHAR(256) PRIMARY KEY,
    course_name VARCHAR(256) NOT NULL,
    hour int,
    course_type int
) CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS teacher_post_paper (
    teacher_id CHAR(5),
    paper_id int,
    teacher_paper_rank int,
    is_cor boolean,
    PRIMARY KEY (teacher_id, paper_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
) CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS teacher_hold_project (
    teacher_id CHAR(5),
    project_id VARCHAR(256),
    teacher_project_rank int,
    teacher_hold_projectmoney float,
    PRIMARY KEY (teacher_id, project_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
) CHARACTER SET utf8mb4;

CREATE TABLE IF NOT EXISTS teacher_teach_course (
    teacher_id CHAR(5),
    course_id VARCHAR(256),
    year int,
    term int,
    own_hour int,
    PRIMARY KEY (teacher_id, course_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
) CHARACTER SET utf8mb4;

insert into teachers value('33333', '张三', '1', '1', '333');
insert into teachers value('44444', '李四', '1', '2', '444');
insert into teachers value('55555', '王五', '2', '3', '555');
insert into courses value('CS001', '计算机系统概论', '60', '1');
insert into courses value('CS011', '计算机系统进阶', '90', '2');
insert into teacher_teach_course value('33333', 'CS001', '2024', '1', '30');
insert into teacher_teach_course value('44444', 'CS001', '2024', '1', '30');
insert into teacher_teach_course value('33333', 'CS011', '2024', '3', '30');
insert into teacher_teach_course value('44444', 'CS011', '2024', '3', '30');
insert into teacher_teach_course value('55555', 'CS011', '2024', '3', '30');