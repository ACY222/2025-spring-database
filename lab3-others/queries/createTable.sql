# My password is ac2718
create database if not exists lab3;
use lab3;

# create all tables

drop table if exists teacher_paper, teacher_course, teacher_project;
drop table if exists teacher, paper, course, project;

create table if not exists teacher (
    teacher_id char(5) primary key,
    teacher_name char(255),
    teacher_gender int,
    teacher_title int,
    check (teacher_gender in (1, 2)),
    check (teacher_title between 1 and 11)
);

create table if not exists paper (
    paper_id int auto_increment primary key,
    paper_name char(255),
    paper_source char(255),
    paper_publish_year int,
    paper_type int,
    paper_level int,
    check (paper_level in (1, 2, 3, 4, 5, 6)),
    check (paper_type in (1, 2, 3, 4))
);

create table if not exists course (
    course_id char(255),
    course_name char(255),
    course_nature int,   # 1 for undergraduate, 2 for graduate
    course_credit_hours int,
    check (course_nature in (1, 2)),
    index idx_id (course_id)   # why it needs to be indexed
);

create table if not exists project (
    project_id char(255) primary key,
    project_name char(255),
    project_source char(255),
    project_type int,
    project_total_fund float,
    project_start_year int,
    project_end_year int,
    check (project_type in (1, 2, 3, 4, 5))
);

create table if not exists teacher_paper (
    teacher_id char(5),
    paper_id int,
    paper_rank int,
    is_corresponding boolean,
    primary key (teacher_id, paper_id),
    foreign key (teacher_id) references teacher(teacher_id),
    foreign key (paper_id) references paper(paper_id),
    unique key (paper_id, paper_rank)      # paperRank is unique for the same paper
);

create table if not exists teacher_project (
    teacher_id char(5),
    project_id char(255),
    project_rank int,
    fund float,

    primary key (teacher_id, project_id),
    foreign key (teacher_id) references teacher(teacher_id),
    foreign key (project_id) references project(project_id),
    unique key (project_id, project_rank)    # projectRank is unique for the same paper
);

create table if not exists teacher_course (
    teacher_id char(5),
    course_id char(255),
    year int,
    semester int,
    teaching_hours int,
    primary key (teacher_id, course_id, semester, year),
    foreign key (teacher_id) references teacher(teacher_id),
    foreign key (course_id) references course(course_id),
    check (semester in (1, 2, 3))
);


# insert some date later
-- 插入教师数据
INSERT INTO teacher (teacher_id, teacher_name, teacher_gender, teacher_title) VALUES
('T0001', '张三', 1, 7),  -- 教授
('T0002', '李四', 1, 6),  -- 副教授
('T0003', '王五', 2, 6),  -- 副教授
('T0004', '赵六', 1, 5),  -- 讲师
('T0005', '钱七', 2, 5),  -- 讲师
('T0006', '孙八', 1, 4),  -- 助教
('T0007', '周九', 2, 7),  -- 教授
('T0008', '吴十', 1, 6),  -- 副教授
('T0009', '郑十一', 2, 5), -- 讲师
('T0010', '王十二', 1, 4); -- 助教

-- 插入论文数据
INSERT INTO paper (paper_name, paper_source, paper_publish_year, paper_type, paper_level) VALUES
('人工智能在医疗影像诊断中的应用', 'IEEE Transactions on Medical Imaging', 2022, 1, 1),
('基于深度学习的自然语言处理技术研究', 'ACM Transactions on Information Systems', 2021, 1, 1),
('大数据分析在智慧城市中的应用', 'Journal of Parallel and Distributed Computing', 2023, 2, 2),
('区块链技术在金融领域的应用研究', 'IEEE Transactions on Services Computing', 2022, 3, 3),
('物联网安全技术研究进展', 'ACM Computing Surveys', 2021, 1, 1),
('云计算架构与应用研究', 'Journal of Cloud Computing', 2023, 2, 2),
('移动应用开发技术研究', 'IEEE Transactions on Mobile Computing', 2022, 3, 3),
('计算机视觉技术研究进展', 'International Journal of Computer Vision', 2021, 1, 1),
('数据挖掘算法研究', 'ACM SIGKDD Explorations Newsletter', 2023, 2, 2),
('网络安全技术研究', 'IEEE Transactions on Information Forensics and Security', 2022, 3, 3);

-- 插入课程数据
INSERT INTO course (course_id, course_name, course_nature, course_credit_hours) VALUES
('CS101', '计算机导论', 1, 3),
('CS102', '程序设计基础', 1, 4),
('CS201', '数据结构', 1, 4),
('CS202', '计算机组成原理', 1, 4),
('CS301', '操作系统', 1, 4),
('CS302', '数据库系统', 1, 4),
('CS401', '人工智能', 1, 3),
('CS501', '高级算法设计', 2, 3),
('CS502', '机器学习', 2, 3),
('CS503', '计算机视觉', 2, 3);

-- 插入项目数据
INSERT INTO project (project_id, project_name, project_source, project_type, project_total_fund, project_start_year, project_end_year) VALUES
('PRJ001', '智能医疗影像分析系统', '国家自然科学基金', 1, 2000000, 2021, 2024),
('PRJ002', '基于区块链的金融安全系统', '教育部', 2, 800000, 2022, 2024),
('PRJ003', '智慧城市大数据平台', '科技部', 1, 1500000, 2021, 2023),
('PRJ004', '物联网安全关键技术研究', '国家863计划', 3, 1200000, 2020, 2023),
('PRJ005', '云计算架构优化研究', '省级科技计划', 4, 500000, 2022, 2023),
('PRJ006', '人工智能教育应用研究', '市级科技计划', 5, 200000, 2023, 2024),
('PRJ007', '大数据分析在医疗领域的应用', '企业合作项目', 2, 300000, 2022, 2023),
('PRJ008', '移动应用开发技术研究', '校级科研基金', 4, 100000, 2023, 2024),
('PRJ009', '计算机视觉算法优化', '国家自然科学基金', 1, 1800000, 2021, 2025),
('PRJ010', '网络安全态势感知系统', '公安部', 3, 1000000, 2022, 2024);

-- 插入教师-论文关联数据
INSERT INTO teacher_paper (teacher_id, paper_id, paper_rank, is_corresponding) VALUES
('T0001', 1, 1, true),
('T0002', 1, 2, false),
('T0003', 2, 1, true),
('T0004', 2, 2, false),
('T0005', 3, 1, true),
('T0006', 3, 2, false),
('T0007', 4, 1, true),
('T0008', 4, 2, false),
('T0009', 5, 1, true),
('T0010', 5, 2, false);

-- 插入教师-项目关联数据
INSERT INTO teacher_project (teacher_id, project_id, project_rank, fund) VALUES
('T0001', 'PRJ001', 1, 800000),
('T0002', 'PRJ001', 2, 500000),
('T0003', 'PRJ002', 1, 300000),
('T0004', 'PRJ002', 2, 250000),
('T0005', 'PRJ003', 1, 600000),
('T0006', 'PRJ003', 2, 400000),
('T0007', 'PRJ004', 1, 500000),
('T0008', 'PRJ004', 2, 300000),
('T0009', 'PRJ005', 1, 200000),
('T0010', 'PRJ005', 2, 150000);

-- 插入教师-课程关联数据
INSERT INTO teacher_course (teacher_id, course_id, year, semester, teaching_hours) VALUES
('T0001', 'CS101', 2023, 1, 48),
('T0002', 'CS102', 2023, 1, 64),
('T0003', 'CS201', 2023, 2, 64),
('T0004', 'CS202', 2023, 2, 64),
('T0005', 'CS301', 2023, 1, 64),
('T0006', 'CS302', 2023, 1, 64),
('T0007', 'CS401', 2023, 2, 48),
('T0008', 'CS501', 2023, 1, 48),
('T0009', 'CS502', 2023, 2, 48),
('T0010', 'CS503', 2023, 1, 48);
