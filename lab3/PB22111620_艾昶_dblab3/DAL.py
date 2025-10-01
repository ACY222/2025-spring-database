# DAL
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import MySQLdb.cursors

def get_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        password="ac2718",
        database="my_lab",
        charset="utf8mb4",
        cursorclass=MySQLdb.cursors.DictCursor
    )

def check_teacher_password(teacher_id, password):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT password FROM teachers WHERE teacher_id = %s"
            cursor.execute(sql, (teacher_id, ))
            result = cursor.fetchone()
            if result is None:
                return False
            db_password = result['password']
            return password == db_password
    finally:
        conn.close()

# 登记发表论文情况
def insert_paper(paper_id, paper_name, source, post_year, paper_type, level):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO papers (paper_id, paper_name, source, post_year, paper_type, level)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (paper_id, paper_name, source, post_year, paper_type, level))
        conn.commit()
    finally:
        conn.close()

def insert_teacher_post_paper(teacher_id, paper_id, rank, is_cor):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO teacher_post_paper (teacher_id, paper_id, teacher_paper_rank, is_cor)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (teacher_id, paper_id, rank, is_cor))
        conn.commit()
    finally:
        conn.close()

def paper_exists(paper_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM papers WHERE paper_id = %s", (paper_id,))
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()

## 检查：一篇论文只能有一位通讯作者，论文的作者排名不能有重复
def one_cor_author(paper_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM teacher_post_paper WHERE paper_id = %s AND is_cor = 1"
    cursor.execute(sql, (paper_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def no_same_rank(paper_id, rank):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM teacher_post_paper WHERE paper_id = %s AND teacher_paper_rank = %s"
    cursor.execute(sql, (paper_id, rank))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

# 删除发表论文情况
def delete_teacher_post_paper(teacher_id, paper_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM teacher_post_paper WHERE teacher_id = %s AND paper_id = %s"
            cursor.execute(sql, (teacher_id, paper_id))
        conn.commit()
    finally:
        conn.close()

# 修改论文
def renew_paper(paper_id, paper_name, source, year, type, level):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE papers SET paper_name = %s, source = %s, post_year = %s, paper_type = %s, level = %s WHERE paper_id = %s"
            cursor.execute(sql, (paper_name, source, year, type, level, paper_id))
        conn.commit()
    finally:
        conn.close()

# 查询论文
def search_paper(paper_id, paper_name, source, year, type, level, teacher_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT p.paper_id, p.paper_name, p.source, 
                       p.post_year, p.paper_type, p.level, t.teacher_id
                FROM papers p
                LEFT JOIN teacher_post_paper t ON p.paper_id = t.paper_id
                WHERE 1=1
            """
            params = []
            if paper_id:
                sql += " AND p.paper_id = %s"
                params.append(paper_id)
            if paper_name:
                sql += " AND p.paper_name LIKE %s"
                params.append(f"%{paper_name}%")
            if source:
                sql += " AND p.source LIKE %s"
                params.append(f"%{source}%")
            if year:
                sql += " AND p.post_year = %s"
                params.append(year)
            if type and type != 'None':
                sql += " AND p.paper_type = %s"
                params.append(type)
            if level and level != 'None':
                sql += " AND p.level = %s"
                params.append(level)
            if teacher_id:
                sql += " AND t.teacher_id = %s"
                params.append(teacher_id)

            cursor.execute(sql, params)
            results = cursor.fetchall()
            return results
        conn.commit()
    finally:
        conn.close()

# 登记承担项目情况
def insert_project(project_id, name, source, type, total_money, start_year, end_year):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO projects (project_id, project_name, project_source, project_type, project_money, start_year, end_year)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (project_id, name, source, type, total_money, start_year, end_year))
        conn.commit()
    finally:
        conn.close()

def insert_teacher_hold_project(teacher_id, project_id, rank, money):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO teacher_hold_project (teacher_id, project_id, teacher_project_rank, teacher_hold_projectmoney)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (teacher_id, project_id, rank, money))
        conn.commit()
    finally:
        conn.close()

def project_exists(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM projects WHERE project_id = %s", (project_id,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        conn.close()

## 检查：排名不能有重复，一个项目中所有教师的承担经费总额应等于项目的总经费
def no_same_project_rank(project_id, rank):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM teacher_hold_project WHERE project_id = %s AND teacher_project_rank = %s"
    cursor.execute(sql, (project_id, rank))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def money_correct(project_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT SUM(teacher_hold_projectmoney) AS total FROM teacher_hold_project WHERE project_id = %s""", (project_id,))
            result = cursor.fetchone()
            total_teacher_money = result['total']

            cursor.execute("""SELECT project_money FROM projects WHERE project_id = %s""", (project_id,))
            result = cursor.fetchone()
            total_project_money = result['project_money']

            if total_teacher_money != total_project_money:
                cursor.execute("""UPDATE projects SET project_money = %s WHERE project_id = %s""", (total_teacher_money, project_id))
                conn.commit()
                return False
            return True
    finally:
        conn.close()

# 删除承担项目情况
def delete_teacher_hold_project(teacher_id, project_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM teacher_hold_project WHERE teacher_id = %s AND project_id = %s"
            cursor.execute(sql, (teacher_id, project_id))
        conn.commit()
    finally:
        conn.close()

# 修改项目
def renew_project(project_id, project_name, source, type, start_year, end_year):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE projects SET project_name = %s, project_source = %s, project_type = %s, start_year = %s , end_year = %s WHERE project_id = %s"
            cursor.execute(sql, (project_name, source, type, start_year, end_year, project_id))
        conn.commit()
    finally:
        conn.close()

# 查询项目
def search_project(project_id, project_name, source, type, money, start_year, end_year, teacher_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT p.project_id, p.project_name, p.project_source, p.project_type, 
                       p.project_money, p.start_year, p.end_year, t.teacher_id
                FROM projects p
                LEFT JOIN teacher_hold_project t ON p.project_id = t.project_id
                WHERE 1=1
            """
            params = []
            if project_id:
                sql += " AND p.project_id = %s"
                params.append(project_id)
            if project_name:
                sql += " AND p.project_name LIKE %s"
                params.append(f"%{project_name}%")
            if source:
                sql += " AND p.project_source LIKE %s"
                params.append(f"%{source}%")
            if type and type != 'None':
                sql += " AND p.project_type = %s"
                params.append(type)
            if money:
                sql += " AND p.project_money = %s"
                params.append(money)
            if start_year:
                sql += " AND p.start_year = %s"
                params.append(start_year)
            if end_year:
                sql += " AND p.end_year = %s"
                params.append(end_year)
            if teacher_id:
                sql += " AND t.teacher_id = %s"
                params.append(teacher_id)

            cursor.execute(sql, params)
            results = cursor.fetchall()
            return results
        conn.commit()
    finally:
        conn.close()

# 登记主讲课程情况
def insert_course(course_id, course_name, hour, course_type):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO courses (course_id, course_name, hour, course_type)
                     VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (course_id, course_name, hour, course_type))
        conn.commit()
    finally:
        conn.close()

def insert_teacher_teach_course(teacher_id, course_id, year, term, own_hour):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """INSERT INTO teacher_teach_course (teacher_id, course_id, year, term, own_hour)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (teacher_id, course_id, year, term, own_hour))
        conn.commit()
    finally:
        conn.close()

def course_exists(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM courses WHERE course_id = %s", (course_id,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        conn.close()

## 检查：一门课程所有教师的主讲学时总额应等于课程的总学时   
def hour_correct(course_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT SUM(own_hour) AS total_hour FROM teacher_teach_course WHERE course_id = %s""", (course_id,))
            result = cursor.fetchone()
            total_hour = result['total_hour']

            cursor.execute("""SELECT hour FROM courses WHERE course_id = %s""", (course_id,))
            result = cursor.fetchone()
            course_hour = result['hour']

            if total_hour != course_hour:
                cursor.execute("""UPDATE courses SET hour = %s WHERE course_id = %s""", (total_hour, course_id))
                conn.commit()
                return False
            return True
    finally:
        conn.close()

# 删除主讲课程情况
def delete_teacher_teach_course(teacher_id, course_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM teacher_teach_course WHERE teacher_id = %s AND course_id = %s"
            cursor.execute(sql, (teacher_id, course_id))
        conn.commit()
    finally:
        conn.close()

# 修改课程
def renew_course(course_id, course_name, hour, type):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE courses SET course_name = %s, hour = %s, course_type = %s WHERE course_id = %s"
            cursor.execute(sql, (course_name, hour, type, course_id))
        conn.commit()
    finally:
        conn.close()

# 查询课程
def search_course(course_id, course_name, hour, type, teacher_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT c.course_id, c.course_name, c.hour, c.course_type, t.teacher_id
                FROM courses c
                LEFT JOIN teacher_teach_course t ON c.course_id = t.course_id
                WHERE 1=1
            """
            params = []
            if course_id:
                sql += " AND c.course_id = %s"
                params.append(course_id)
            if course_name:
                sql += " AND c.course_name LIKE %s"
                params.append(f"%{course_name}%")
            if hour:
                sql += " AND c.hour = %s"
                params.append(hour)
            if type and type != 'None':
                sql += " AND c.course_type = %s"
                params.append(type)
            if teacher_id:
                sql += " AND t.teacher_id = %s"
                params.append(teacher_id)

            cursor.execute(sql, params)
            results = cursor.fetchall()
            return results
        conn.commit()
    finally:
        conn.close()

# 查询统计
def get_teacher_statistics(teacher_id, from_year, to_year):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        result = {}

        # 论文
        cursor.execute("""
            SELECT p.paper_id, p.paper_name, p.source, p.post_year, p.paper_type, p.level, tpp.teacher_paper_rank, tpp.is_cor
            FROM teacher_post_paper tpp
            JOIN papers p ON tpp.paper_id = p.paper_id
            WHERE tpp.teacher_id = %s AND p.post_year BETWEEN %s AND %s
            ORDER BY p.post_year DESC
        """, (teacher_id, from_year, to_year))
        result['papers'] = cursor.fetchall()

        # 项目
        cursor.execute("""
            SELECT p.project_id, p.project_name, p.project_source, p.project_type, p.start_year, p.end_year, thp.teacher_project_rank, thp.teacher_hold_projectmoney
            FROM teacher_hold_project thp
            JOIN projects p ON thp.project_id = p.project_id
            WHERE thp.teacher_id = %s AND p.start_year <= %s AND p.end_year >= %s
            ORDER BY p.start_year DESC
        """, (teacher_id, to_year, from_year))
        result['projects'] = cursor.fetchall()

        # 课程
        cursor.execute("""
            SELECT c.course_id, c.course_name, c.course_type, ttc.year, ttc.term, ttc.own_hour
            FROM teacher_teach_course ttc
            JOIN courses c ON ttc.course_id = c.course_id
            WHERE ttc.teacher_id = %s AND ttc.year BETWEEN %s AND %s
            ORDER BY ttc.year DESC
        """, (teacher_id, from_year, to_year))
        result['courses'] = cursor.fetchall()

        return result

    finally:
        cursor.close()
        conn.close()

def fetch_all_from_table(table_name):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            results = cursor.fetchall()
            return results
    finally:
        conn.close()
