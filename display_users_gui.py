import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_PATH = "instance/database.db"
ROWS_PER_PAGE = 5

class UserTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Signup Table")
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        
        self.page = 1
        self.total_pages = 1
        self.search_text = ""

        # Search frame
        search_frame = tk.Frame(root)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Search username/email:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(search_frame, text="Search", command=self.search)
        search_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(search_frame, text="Clear", command=self.clear_search)
        clear_btn.pack(side=tk.LEFT, padx=5)

        # Table (Treeview)
        self.tree = ttk.Treeview(root, columns=("id", "user_id", "username", "email", "phone", "ip", "device"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120)
        self.tree.pack(pady=10)

        # Pagination buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.first_btn = tk.Button(btn_frame, text="First", command=self.first_page)
        self.first_btn.pack(side=tk.LEFT, padx=5)

        self.prev_btn = tk.Button(btn_frame, text="Previous", command=self.prev_page)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.page_label = tk.Label(btn_frame, text="Page 1/1")
        self.page_label.pack(side=tk.LEFT, padx=5)

        self.next_btn = tk.Button(btn_frame, text="Next", command=self.next_page)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.last_btn = tk.Button(btn_frame, text="Last", command=self.last_page)
        self.last_btn.pack(side=tk.LEFT, padx=5)

        # Exit button
        exit_btn = tk.Button(root, text="Exit", command=self.exit_app)
        exit_btn.pack(pady=10)

        self.update_total_pages()
        self.load_data()

    def update_total_pages(self):
        if self.search_text:
            query = "SELECT COUNT(*) FROM user_signup WHERE username LIKE ? OR email LIKE ?"
            like_pattern = f"%{self.search_text}%"
            self.cursor.execute(query, (like_pattern, like_pattern))
        else:
            self.cursor.execute("SELECT COUNT(*) FROM user_signup")
        total_rows = self.cursor.fetchone()[0]
        self.total_pages = max(1, (total_rows + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE)
        if self.page > self.total_pages:
            self.page = self.total_pages

    def load_data(self):
        self.tree.delete(*self.tree.get_children())

        offset = (self.page - 1) * ROWS_PER_PAGE
        if self.search_text:
            query = """
                SELECT id, user_id, username, email, phone, ip, device 
                FROM user_signup
                WHERE username LIKE ? OR email LIKE ?
                ORDER BY id
                LIMIT ? OFFSET ?
            """
            like_pattern = f"%{self.search_text}%"
            self.cursor.execute(query, (like_pattern, like_pattern, ROWS_PER_PAGE, offset))
        else:
            query = """
                SELECT id, user_id, username, email, phone, ip, device 
                FROM user_signup
                ORDER BY id
                LIMIT ? OFFSET ?
            """
            self.cursor.execute(query, (ROWS_PER_PAGE, offset))

        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)
        self.page_label.config(text=f"Page {self.page}/{self.total_pages}")

        # Disable buttons appropriately
        self.first_btn.config(state=tk.NORMAL if self.page > 1 else tk.DISABLED)
        self.prev_btn.config(state=tk.NORMAL if self.page > 1 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.page < self.total_pages else tk.DISABLED)
        self.last_btn.config(state=tk.NORMAL if self.page < self.total_pages else tk.DISABLED)

    def first_page(self):
        self.page = 1
        self.load_data()

    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.load_data()

    def next_page(self):
        if self.page < self.total_pages:
            self.page += 1
            self.load_data()

    def last_page(self):
        self.page = self.total_pages
        self.load_data()

    def search(self):
        self.search_text = self.search_entry.get().strip()
        self.page = 1
        self.update_total_pages()
        self.load_data()

    def clear_search(self):
        self.search_text = ""
        self.search_entry.delete(0, tk.END)
        self.page = 1
        self.update_total_pages()
        self.load_data()

    def exit_app(self):
        self.conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UserTableApp(root)
    root.mainloop()
