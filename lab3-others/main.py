import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from mysql.connector import Error
import docx
import xlsxwriter
from io import BytesIO
import os
from datetime import datetime

class TeacherResearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("教师教学科研登记系统")
        self.root.geometry("800x600")           # window size

        # 数据库配置
        self.db_config = {          # I'm not sure how to config
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'ac2718',
            'database': 'lab3'
        }

        # 创建主菜单
        self.create_menu()

        # 创建主界面
        self.create_main_frame()

    def create_menu(self):
        # 创建菜单栏
        menu_bar = tk.Menu(self.root)

        # 文件菜单
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="查询统计", command=self.show_statistics)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menu_bar.add_cascade(label="文件", menu=file_menu)

        # 数据管理菜单
        data_menu = tk.Menu(menu_bar, tearoff=0)
        data_menu.add_command(label="论文管理", command=self.show_papers)
        data_menu.add_command(label="项目管理", command=self.show_projects)
        data_menu.add_command(label="课程管理", command=self.show_courses)
        menu_bar.add_cascade(label="数据管理", menu=data_menu)

        # 帮助菜单
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menu_bar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=menu_bar)

    def create_main_frame(self):
        # 创建主界面
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(6, weight=1)  # 作者信息区域可扩展

        # 欢迎信息
        ttk.Label(main_frame, text="欢迎使用教师教学科研登记系统", font=("Arial", 16)).pack(pady=20)

        # 功能按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="论文管理", command=self.show_papers).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="项目管理", command=self.show_projects).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="课程管理", command=self.show_courses).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="查询统计", command=self.show_statistics).pack(side=tk.LEFT, padx=10)
        # ttk.Button(btn_frame, text="导出数据", command=self.export_data).pack(side=tk.LEFT, padx=10)

    def show_papers(self):
        paper_window = tk.Toplevel(self.root)
        paper_window.title("论文管理")
        paper_window.geometry("800x600")

        # 创建顶部按钮区域
        btn_frame = ttk.Frame(paper_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(btn_frame, text="添加论文", command=lambda: self.add_paper(paper_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑论文", command=lambda: self.edit_paper(paper_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除论文", command=lambda: self.delete_paper(paper_window)).pack(side=tk.LEFT, padx=5)

        # 创建表格显示论文列表
        columns = ("paper_name", "paper_publish_year", "paper_level", "paper_source", "paper_type")
        self.papers_tree = ttk.Treeview(paper_window, columns=columns, show="headings")
        # 设置列标题
        self.papers_tree.heading("paper_name", text="标题")
        self.papers_tree.heading("paper_publish_year", text="发表年份")
        self.papers_tree.heading("paper_level", text="级别")
        self.papers_tree.heading("paper_source", text="发表源")
        self.papers_tree.heading("paper_type", text="类型")

        # 设置列宽
        self.papers_tree.column("paper_name", width=200)
        self.papers_tree.column("paper_publish_year", width=80)
        self.papers_tree.column("paper_level", width=80)
        self.papers_tree.column("paper_source", width=150)
        self.papers_tree.column("paper_type", width=100)

        self.papers_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 加载论文数据
        self.load_papers(self.papers_tree)

    def load_papers(self, tree):
        # 清空现有数据
        for item in tree.get_children():
            tree.delete(item)

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM paper")
            papers = cursor.fetchall()

            for paper in papers:
                tree.insert("", tk.END, values=(
                    paper["paper_name"],
                    paper["paper_publish_year"],
                    self.get_level_name(paper["paper_level"]),
                    paper["paper_source"],
                    self.get_type_name(paper["paper_type"])
                ))
        except Error as e:
            messagebox.showerror("错误", f"加载论文数据失败: {e}")
        finally:
            conn.close()

    def add_paper(self, parent_window):
        # 添加论文弹窗
        paper_dialog = tk.Toplevel(parent_window)
        paper_dialog.title("添加论文")
        paper_dialog.geometry("600x500")
        paper_dialog.transient(parent_window)
        paper_dialog.grab_set()

        # 创建表单
        form_frame = ttk.Frame(paper_dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # 填写表单信息
        ttk.Label(form_frame, text="标题:").grid(row=0, column=0, sticky=tk.W, pady=5)
        title_entry = ttk.Entry(form_frame, width=40)
        title_entry.insert(0, "title")
        title_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="发表年份:").grid(row=1, column=0, sticky=tk.W, pady=5)
        year_entry = ttk.Entry(form_frame, width=10)
        year_entry.insert(0, datetime.now().year)
        year_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="级别:").grid(row=2, column=0, sticky=tk.W, pady=5)
        level_var = tk.StringVar()
        level_combo = ttk.Combobox(form_frame, textvariable=level_var, width=15, state="readonly")
        level_combo['values'] = ("1-CCF-A", "2-CCF-B", "3-CCF-C", "4-中文CCF-A", "5-中文CCF-B", "6-无级别")
        level_combo.set("6-无级别")
        level_combo.grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="发表源:").grid(row=3, column=0, sticky=tk.W, pady=5)
        source_entry = ttk.Entry(form_frame, width=40)
        source_entry.insert(0, "USTC")
        source_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="类型:").grid(row=4, column=0, sticky=tk.W, pady=5)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, width=15, state="readonly")
        type_combo['values'] = ("1-full paper", "2-short paper", "3-poster paper", "4-demo paper")
        type_combo.set("4-demo paper")
        type_combo.grid(row=4, column=1, sticky=tk.W, pady=5)

        # 作者信息
        ttk.Label(form_frame, text="作者信息:").grid(row=5, column=0, sticky=tk.W, pady=10)

        # 作者列表
        authors_frame = ttk.LabelFrame(form_frame, text="作者列表")
        authors_frame.grid(row=6, column=0, columnspan=2, sticky=tk.W + tk.E, pady=5)

        self.author_rows = []
        self.add_author_row(authors_frame, 0)

        # 添加作者按钮
        add_author_btn = ttk.Button(authors_frame, text="添加作者", command=lambda: self.add_author_row(authors_frame, len(self.author_rows)))
        add_author_btn.grid(row=7, column=0, columnspan=5, pady=5)

        # 按钮区域
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20)

        def save_paper():
            # 获取表单数据
            title = title_entry.get().strip()
            publish_year = year_entry.get().strip()
            level_text = level_var.get()
            source = source_entry.get().strip()
            type_text = type_var.get()

            # 数据验证
            if not title:
                messagebox.showerror("错误", "论文标题不能为空")
                return

            try:
                publish_year = int(publish_year)
                if publish_year < 1900 or publish_year > datetime.now().year:
                    raise ValueError("年份范围无效")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的发表年份")
                return

            if not level_text:
                messagebox.showerror("错误", "请选择论文级别")
                return

            # 将级别文本转换为数字
            level_map = {
                "1-CCF-A": 1, "2-CCF-B": 2, "3-CCF-C": 3,
                "4-中文CCF-A": 4, "5-中文CCF-B": 5, "6-无级别": 6
            }
            level = level_map.get(level_text)

            if not type_text:
                messagebox.showerror("错误", "请选择论文类型")
                return

            # 将类型文本转换为数字
            type_map = {
                "1-full paper": 1,
                "2-short paper": 2,
                "3-poster paper": 3,
                "4-demo paper": 4
            }
            paper_type = type_map.get(type_text)

            # 检查通讯作者数量
            corr_count = 0
            ranks = []
            for teacher_id_entry, rank_entry, is_corr_var in self.author_rows:
                is_corresponding = is_corr_var.get()
                if is_corresponding:
                    corr_count += 1
                rank = rank_entry.get().strip()
                try:
                    rank = int(rank)
                    if rank <= 0:
                        raise ValueError("排名必须为正整数")
                    ranks.append(rank)
                except ValueError:
                    messagebox.showerror("错误", "请输入有效的排名")
                    return
            if corr_count > 1:
                messagebox.showerror("错误", "一篇论文只能有一位通讯作者")
                return

            # 检查排名是否重复
            if len(set(ranks)) != len(ranks):
                messagebox.showerror("错误", "论文的作者排名不能有重复")
                return 

            # 连接数据库
            conn = self.get_db_connection()
            if not conn:
                return

            try:
                cursor = conn.cursor()

                # 插入论文数据
                cursor.execute(
                    "INSERT INTO paper (paper_name, paper_publish_year, paper_level, paper_source, paper_type) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (title, publish_year, level, source, paper_type)
                )
                paper_id = cursor.lastrowid

                # 处理作者信息
                for teacher_id_entry, rank_entry, is_corr_var in self.author_rows:
                    teacher_id = teacher_id_entry.get().strip()
                    rank = rank_entry.get().strip()
                    is_corresponding = is_corr_var.get()

                    # 验证作者信息
                    if not teacher_id:
                        messagebox.showerror("错误", "教师工号不能为空")
                        return

                    try:
                        rank = int(rank)
                        if rank <= 0:
                            raise ValueError("排名必须为正整数")
                    except ValueError:
                        messagebox.showerror("错误", "请输入有效的排名")
                        return

                    # 检查教师是否存在
                    cursor.execute("SELECT * FROM teacher WHERE teacher_id = %s", (teacher_id,))
                    if not cursor.fetchone():
                        messagebox.showerror("错误", f"教师工号 {teacher_id} 不存在")
                        return

                    # 插入作者关系
                    cursor.execute(
                        "INSERT INTO teacher_paper (teacher_id, paper_id, paper_rank, is_corresponding) "
                        "VALUES (%s, %s, %s, %s)",
                        (teacher_id, paper_id, rank, is_corresponding)
                    )

                conn.commit()
                messagebox.showinfo("成功", "论文添加成功！")
                paper_dialog.destroy()

                # 刷新主窗口的论文列表
                if hasattr(self, 'papers_tree'):
                    self.load_papers(self.papers_tree)

            except Error as e:
                conn.rollback()
                messagebox.showerror("错误", f"保存论文失败: {e}")
            finally:
                conn.close()

        ttk.Button(btn_frame, text="保存", command=save_paper).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", command=paper_dialog.destroy).pack(side=tk.LEFT, padx=10)

    def add_author_row(self, authors_frame, row):
        ttk.Label(authors_frame, text="教师工号:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        teacher_id_entry = ttk.Entry(authors_frame, width=10)
        teacher_id_entry.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(authors_frame, text="排名:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        rank_entry = ttk.Entry(authors_frame, width=5)
        rank_entry.grid(row=row, column=3, sticky=tk.W, padx=5, pady=5)

        is_corr_var = tk.BooleanVar()
        corr_check = ttk.Checkbutton(authors_frame, text="通讯作者", variable=is_corr_var)
        corr_check.grid(row=row, column=4, sticky=tk.W, padx=5, pady=5)

        self.author_rows.append((teacher_id_entry, rank_entry, is_corr_var))

    def delete_paper(self, parent_window):
        selected_item = self.papers_tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请选择要删除的论文")
            return

        confirm = messagebox.askyesno("确认", "确定要删除选中的论文吗？")
        if not confirm:
            return

        values = self.papers_tree.item(selected_item, 'values')
        title = values[0]

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor()
            # 获取论文ID
            cursor.execute("SELECT paper_id FROM paper WHERE paper_name = %s", (title,))
            paper_id = cursor.fetchone()[0]

            # 删除教师与论文的关联
            cursor.execute("DELETE FROM teacher_paper WHERE paper_id = %s", (paper_id,))
            # 删除论文
            cursor.execute("DELETE FROM paper WHERE paper_id = %s", (paper_id,))

            conn.commit()
            messagebox.showinfo("成功", "论文删除成功！")
            # 刷新论文列表
            self.load_papers(self.papers_tree)
        except Error as e:
            conn.rollback()
            messagebox.showerror("错误", f"删除论文失败: {e}")
        finally:
            conn.close()

    def edit_paper(self, parent_window):
        selected_item = self.papers_tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请选择要编辑的论文")
            return

        values = self.papers_tree.item(selected_item, 'values')
        title = values[0]

        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor(dictionary=True)
            # 获取论文信息
            cursor.execute("SELECT * FROM paper WHERE paper_name = %s", (title,))
            paper = cursor.fetchone()

            # 打开编辑窗口
            edit_dialog = tk.Toplevel(parent_window)
            edit_dialog.title("编辑论文")
            edit_dialog.geometry("600x500")
            edit_dialog.transient(parent_window)
            edit_dialog.grab_set()

            # 创建表单
            form_frame = ttk.Frame(edit_dialog, padding="20")
            form_frame.pack(fill=tk.BOTH, expand=True)

            # 填写表单信息
            ttk.Label(form_frame, text="标题:").grid(row=0, column=0, sticky=tk.W, pady=5)
            title_entry = ttk.Entry(form_frame, width=40)
            title_entry.insert(0, paper["paper_name"])
            title_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

            ttk.Label(form_frame, text="发表年份:").grid(row=1, column=0, sticky=tk.W, pady=5)
            year_entry = ttk.Entry(form_frame, width=10)
            year_entry.insert(0, paper["paper_publish_year"])
            year_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

            ttk.Label(form_frame, text="级别:").grid(row=2, column=0, sticky=tk.W, pady=5)
            level_var = tk.StringVar()
            level_combo = ttk.Combobox(form_frame, textvariable=level_var, width=15, state="readonly")
            level_combo['values'] = ("1-CCF-A", "2-CCF-B", "3-CCF-C", "4-中文CCF-A", "5-中文CCF-B", "6-无级别")
            level_combo.set(self.get_level_name(paper["paper_level"]))
            level_combo.grid(row=2, column=1, sticky=tk.W, pady=5)

            ttk.Label(form_frame, text="发表源:").grid(row=3, column=0, sticky=tk.W, pady=5)
            source_entry = ttk.Entry(form_frame, width=40)
            source_entry.insert(0, paper["paper_source"])
            source_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

            ttk.Label(form_frame, text="类型:").grid(row=4, column=0, sticky=tk.W, pady=5)
            type_var = tk.StringVar()
            type_combo = ttk.Combobox(form_frame, textvariable=type_var, width=15, state="readonly")
            type_combo['values'] = ("1-full paper", "2-short paper", "3-poster paper", "4-demo paper")
            type_combo.set(self.get_type_name(paper["paper_type"]))
            type_combo.grid(row=4, column=1, sticky=tk.W, pady=5)

            # 作者信息
            ttk.Label(form_frame, text="作者信息:").grid(row=5, column=0, sticky=tk.W, pady=10)

            # 作者列表
            authors_frame = ttk.LabelFrame(form_frame, text="作者列表")
            authors_frame.grid(row=6, column=0, columnspan=2, sticky=tk.W + tk.E, pady=5)

            self.author_rows = []
            # 获取作者信息
            cursor.execute("SELECT * FROM teacher_paper WHERE paper_id = %s", (paper["paper_id"],))
            authors = cursor.fetchall()
            for i, author in enumerate(authors):
                self.add_author_row(authors_frame, i)
                self.author_rows[i][0].insert(0, author["teacher_id"])
                self.author_rows[i][1].insert(0, author["paper_rank"])
                self.author_rows[i][2].set(author["is_corresponding"])

            # 添加作者按钮
            add_author_btn = ttk.Button(authors_frame, text="添加作者", command=lambda: self.add_author_row(authors_frame, len(self.author_rows)))
            add_author_btn.grid(row=len(authors)+1, column=0, columnspan=5, pady=5)

            # 按钮区域
            btn_frame = ttk.Frame(form_frame)
            btn_frame.grid(row=len(authors)+2, column=0, columnspan=2, pady=20)

            def save_edited_paper():
                # 获取表单数据
                new_title = title_entry.get().strip()
                publish_year = year_entry.get().strip()
                level_text = level_var.get()
                source = source_entry.get().strip()
                type_text = type_var.get()

                # 数据验证
                if not new_title:
                    messagebox.showerror("错误", "论文标题不能为空")
                    return

                try:
                    publish_year = int(publish_year)
                    if publish_year < 1900 or publish_year > datetime.now().year:
                        raise ValueError("年份范围无效")
                except ValueError:
                    messagebox.showerror("错误", "请输入有效的发表年份")
                    return

                if not level_text:
                    messagebox.showerror("错误", "请选择论文级别")
                    return

                # 将级别文本转换为数字
                level_map = {
                    "1-CCF-A": 1, "2-CCF-B": 2, "3-CCF-C": 3,
                    "4-中文CCF-A": 4, "5-中文CCF-B": 5, "6-无级别": 6
                }
                level = level_map.get(level_text)

                if not type_text:
                    messagebox.showerror("错误", "请选择论文类型")
                    return

                # 将类型文本转换为数字
                type_map = {
                    "1-full paper": 1,
                    "2-short paper": 2,
                    "3-poster paper": 3,
                    "4-demo paper": 4
                }
                paper_type = type_map.get(type_text)

                # 检查通讯作者数量
                corr_count = 0
                ranks = []
                for teacher_id_entry, rank_entry, is_corr_var in self.author_rows:
                    is_corresponding = is_corr_var.get()
                    if is_corresponding:
                        corr_count += 1
                    rank = rank_entry.get().strip()
                    try:
                        rank = int(rank)
                        if rank <= 0:
                            raise ValueError("排名必须为正整数")
                        ranks.append(rank)
                    except ValueError:
                        messagebox.showerror("错误", "请输入有效的排名")
                        return
                if corr_count > 1:
                    messagebox.showerror("错误", "一篇论文只能有一位通讯作者")
                    return

                # 检查排名是否重复
                if len(set(ranks)) != len(ranks):
                    messagebox.showerror("错误", "论文的作者排名不能有重复")
                    return 

                try:
                    # 更新论文数据
                    cursor.execute(
                        "UPDATE paper SET paper_name = %s, paper_publish_year = %s, paper_level = %s, paper_source = %s, paper_type = %s "
                        "WHERE paper_id = %s",
                        (new_title, publish_year, level, source, paper_type, paper["paper_id"])
                    )

                    # 删除原有的作者关系
                    cursor.execute("DELETE FROM teacher_paper WHERE paper_id = %s", (paper["paper_id"],))

                    # 处理作者信息
                    for teacher_id_entry, rank_entry, is_corr_var in self.author_rows:
                        teacher_id = teacher_id_entry.get().strip()
                        rank = rank_entry.get().strip()
                        is_corresponding = is_corr_var.get()

                        # 验证作者信息
                        if not teacher_id:
                            messagebox.showerror("错误", "教师工号不能为空")
                            return

                        try:
                            rank = int(rank)
                            if rank <= 0:
                                raise ValueError("排名必须为正整数")
                        except ValueError:
                            messagebox.showerror("错误", "请输入有效的排名")
                            return

                        # 检查教师是否存在
                        cursor.execute("SELECT * FROM teacher WHERE teacher_id = %s", (teacher_id,))
                        if not cursor.fetchone():
                            messagebox.showerror("错误", f"教师工号 {teacher_id} 不存在")
                            return

                        # 插入新的作者关系
                        cursor.execute(
                            "INSERT INTO teacher_paper (teacher_id, paper_id, paper_rank, is_corresponding) "
                            "VALUES (%s, %s, %s, %s)",
                            (teacher_id, paper["paper_id"], rank, is_corresponding)
                        )

                    conn.commit()
                    messagebox.showinfo("成功", "论文编辑成功！")
                    edit_dialog.destroy()

                    # 刷新主窗口的论文列表
                    if hasattr(self, 'papers_tree'):
                        self.load_papers(self.papers_tree)

                except Error as e:
                    conn.rollback()
                    messagebox.showerror("错误", f"保存编辑后的论文失败: {e}")

            ttk.Button(btn_frame, text="保存", command=save_edited_paper).pack(side=tk.LEFT, padx=10)
            ttk.Button(btn_frame, text="取消", command=edit_dialog.destroy).pack(side=tk.LEFT, padx=10)

        except Error as e:
            messagebox.showerror("错误", f"加载论文信息失败: {e}")
        finally:
            conn.close()

    # 以下是各功能的实现方法
    def show_projects(self):
        # 项目管理窗口
        project_window = tk.Toplevel(self.root)
        project_window.title("项目管理")
        project_window.geometry("800x600")

        # 创建项目列表和操作按钮
        # ...

    def show_courses(self):
        # 课程管理窗口
        course_window = tk.Toplevel(self.root)
        course_window.title("课程管理")
        course_window.geometry("800x600")

        # 创建课程列表和操作按钮
        # ...

    def show_statistics(self):
        # 查询统计窗口
        stats_window = tk.Toplevel(self.root)
        stats_window.title("查询统计")
        stats_window.geometry("800x600")

        # 创建查询表单和结果显示
        # ...

    def show_about(self):
        # 关于窗口
        messagebox.showinfo("关于", "教师教学科研登记系统 v1.0\n\n基于Python和MySQL开发")

    # 数据库操作方法
    def get_db_connection(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except Error as e:
            messagebox.showerror("数据库连接错误", f"无法连接到数据库: {e}")
            return None

    def get_level_name(self, level):
        level_map = {
            1: "1-CCF-A",
            2: "2-CCF-B",
            3: "3-CCF-C",
            4: "4-中文CCF-A",
            5: "5-中文CCF-B",
            6: "6-无级别"
        }
        return level_map.get(level, "未知级别")

    def get_type_name(self, type):
        type_map = {
            1: "1-full paper",
            2: "2-short paper",
            3: "3-poster paper",
            4: "4-demo paper"
        }
        return type_map.get(type, "未知类型")

# 启动应用
if __name__ == "__main__":
    root = tk.Tk()
    app = TeacherResearchApp(root)
    root.mainloop()
