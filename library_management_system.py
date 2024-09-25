import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime

# Set up the database
conn = sqlite3.connect('library.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT, 
    password TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT, 
    author TEXT, 
    year INTEGER, 
    isbn TEXT,
    issued_to TEXT,
    issue_date TEXT)''')
conn.commit()

# Check if the admin exists and create it if not
c.execute("SELECT * FROM admin WHERE username=?", ('admin',))
if c.fetchone() is None:
    c.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ('admin', 'admin123'))
    conn.commit()

def login():
    username = entry_username.get()
    password = entry_password.get()

    c.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    
    if result:
        open_admin_panel(result[1])
    else:
        messagebox.showerror("Error", "Invalid Credentials. Please try again.")

def open_admin_panel(admin_name):
    login_window.withdraw()

    admin_window = tk.Toplevel()
    admin_window.title("Admin Dashboard")
    admin_window.configure(bg='black')

    tk.Label(admin_window, text=f"Logged in as: {admin_name}", bg='black', fg='white').pack(pady=10)
    tk.Label(admin_window, text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bg='black', fg='white').pack(pady=10)

    tk.Button(admin_window, text="Add Books", width=20, command=add_books).pack(pady=5)
    tk.Button(admin_window, text="Issue Books", width=20, command=issue_books).pack(pady=5)
    tk.Button(admin_window, text="Edit Books", width=20, command=edit_books).pack(pady=5)
    tk.Button(admin_window, text="Return Books", width=20, command=return_books).pack(pady=5)
    tk.Button(admin_window, text="Delete Books", width=20, command=delete_books).pack(pady=5)
    tk.Button(admin_window, text="Search Books", width=20, command=search_books).pack(pady=5)
    tk.Button(admin_window, text="Show All Books", width=20, command=show_books).pack(pady=5)
    tk.Button(admin_window, text="Log Out", width=20, command=lambda: logout(admin_window)).pack(pady=5)

def add_books():
    def save_book():
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()
        isbn = entry_isbn.get()

        c.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)", (title, author, year, isbn))
        conn.commit()
        messagebox.showinfo("Success", "Book added successfully")
        add_window.destroy()

    add_window = tk.Toplevel()
    add_window.title("Add a New Book")
    add_window.configure(bg='black')

    tk.Label(add_window, text="Title:", bg='black', fg='white').grid(row=0, column=0)
    entry_title = tk.Entry(add_window)
    entry_title.grid(row=0, column=1)

    tk.Label(add_window, text="Author:", bg='black', fg='white').grid(row=1, column=0)
    entry_author = tk.Entry(add_window)
    entry_author.grid(row=1, column=1)

    tk.Label(add_window, text="Year:", bg='black', fg='white').grid(row=2, column=0)
    entry_year = tk.Entry(add_window)
    entry_year.grid(row=2, column=1)

    tk.Label(add_window, text="ISBN:", bg='black', fg='white').grid(row=3, column=0)
    entry_isbn = tk.Entry(add_window)
    entry_isbn.grid(row=3, column=1)

    tk.Button(add_window, text="Save Book", command=save_book).grid(row=4, column=0, columnspan=2)

def issue_books():
    def issue_book():
        student_name = entry_student_name.get()
        c.execute("SELECT COUNT(*) FROM books WHERE issued_to=?", (student_name,))
        count = c.fetchone()[0]

        if count < 3:
            book_id = entry_book_id.get()
            c.execute("SELECT * FROM books WHERE id=? AND issued_to IS NULL", (book_id,))
            book = c.fetchone()

            if book:
                issue_date = datetime.datetime.now().strftime("%Y-%m-%d")
                c.execute("UPDATE books SET issued_to=?, issue_date=? WHERE id=?", (student_name, issue_date, book_id))
                conn.commit()
                messagebox.showinfo("Success", "Book issued successfully")
                issue_window.destroy()
            else:
                messagebox.showerror("Error", "Book not found or already issued")
        else:
            messagebox.showerror("Error", "Max limit reached (3 books)")

    issue_window = tk.Toplevel()
    issue_window.title("Issue Book")
    issue_window.configure(bg='black')

    tk.Label(issue_window, text="Book ID:", bg='black', fg='white').grid(row=0, column=0)
    entry_book_id = tk.Entry(issue_window)
    entry_book_id.grid(row=0, column=1)

    tk.Label(issue_window, text="Student Name:", bg='black', fg='white').grid(row=1, column=0)
    entry_student_name = tk.Entry(issue_window)
    entry_student_name.grid(row=1, column=1)

    tk.Button(issue_window, text="Issue Book", command=issue_book).grid(row=2, column=0, columnspan=2)

def edit_books():
    def update_book():
        book_id = entry_book_id.get()
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()
        isbn = entry_isbn.get()

        c.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, book_id))
        conn.commit()
        messagebox.showinfo("Success", "Book updated successfully")
        edit_window.destroy()

    edit_window = tk.Toplevel()
    edit_window.title("Edit Book")
    edit_window.configure(bg='black')

    tk.Label(edit_window, text="Book ID:", bg='black', fg='white').grid(row=0, column=0)
    entry_book_id = tk.Entry(edit_window)
    entry_book_id.grid(row=0, column=1)

    tk.Button(edit_window, text="Load Book", command=lambda: load_book(entry_book_id.get())).grid(row=1, column=0, columnspan=2)

    tk.Label(edit_window, text="Title:", bg='black', fg='white').grid(row=2, column=0)
    entry_title = tk.Entry(edit_window)
    entry_title.grid(row=2, column=1)

    tk.Label(edit_window, text="Author:", bg='black', fg='white').grid(row=3, column=0)
    entry_author = tk.Entry(edit_window)
    entry_author.grid(row=3, column=1)

    tk.Label(edit_window, text="Year:", bg='black', fg='white').grid(row=4, column=0)
    entry_year = tk.Entry(edit_window)
    entry_year.grid(row=4, column=1)

    tk.Label(edit_window, text="ISBN:", bg='black', fg='white').grid(row=5, column=0)
    entry_isbn = tk.Entry(edit_window)
    entry_isbn.grid(row=5, column=1)

    tk.Button(edit_window, text="Update Book", command=update_book).grid(row=6, column=0, columnspan=2)

def load_book(book_id):
    c.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = c.fetchone()
    if book:
        entry_title.delete(0, tk.END)
        entry_author.delete(0, tk.END)
        entry_year.delete(0, tk.END)
        entry_isbn.delete(0, tk.END)
        
        entry_title.insert(0, book[1])
        entry_author.insert(0, book[2])
        entry_year.insert(0, book[3])
        entry_isbn.insert(0, book[4])
    else:
        messagebox.showerror("Error", "Book not found")

def return_books():
    def return_book():
        book_id = entry_book_id.get()

        c.execute("SELECT * FROM books WHERE id=? AND issued_to IS NOT NULL", (book_id,))
        book = c.fetchone()

        if book:
            fine = calculate_fine(book[6])  # book[6] is the issue_date
            c.execute("UPDATE books SET issued_to=NULL, issue_date=NULL WHERE id=?", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", f"Book returned successfully. Fine: ${fine}")
            return_window.destroy()
        else:
            messagebox.showerror("Error", "Book not found or not issued")

    return_window = tk.Toplevel()
    return_window.title("Return Book")
    return_window.configure(bg='black')

    tk.Label(return_window, text="Book ID:", bg='black', fg='white').grid(row=0, column=0)
    entry_book_id = tk.Entry(return_window)
    entry_book_id.grid(row=0, column=1)

    tk.Button(return_window, text="Return Book", command=return_book).grid(row=1, column=0, columnspan=2)

def calculate_fine(issue_date):
    issue_date = datetime.datetime.strptime(issue_date, "%Y-%m-%d")
    days_difference = (datetime.datetime.now() - issue_date).days
    if days_difference > 7:  # Assuming 7 days for free
        fine = (days_difference - 7) * 1  # $1 per day after 7 days
        return fine
    return 0

def delete_books():
    def delete_book():
        book_id = entry_book_id.get()
        c.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book deleted successfully")
        delete_window.destroy()

    delete_window = tk.Toplevel()
    delete_window.title("Delete Book")
    delete_window.configure(bg='black')

    tk.Label(delete_window, text="Book ID:", bg='black', fg='white').grid(row=0, column=0)
    entry_book_id = tk.Entry(delete_window)
    entry_book_id.grid(row=0, column=1)

    tk.Button(delete_window, text="Delete Book", command=delete_book).grid(row=1, column=0, columnspan=2)

def search_books():
    def search_book():
        search_term = entry_search_term.get()
        c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", (f'%{search_term}%', f'%{search_term}%'))
        rows = c.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        for row in rows:
            tree.insert('', 'end', values=row)

    search_window = tk.Toplevel()
    search_window.title("Search Books")
    search_window.configure(bg='black')

    tk.Label(search_window, text="Search Term:", bg='black', fg='white').grid(row=0, column=0)
    entry_search_term = tk.Entry(search_window)
    entry_search_term.grid(row=0, column=1)

    tk.Button(search_window, text="Search", command=search_book).grid(row=1, column=0, columnspan=2)

    tree = ttk.Treeview(search_window, columns=("ID", "Title", "Author", "Year", "ISBN", "Issued To", "Issue Date"), show='headings')
    tree.grid(row=2, column=0, columnspan=2)

    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Year", text="Year")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Issued To", text="Issued To")
    tree.heading("Issue Date", text="Issue Date")

def show_books():
    show_window = tk.Toplevel()
    show_window.title("All Books")
    show_window.configure(bg='black')

    tree = ttk.Treeview(show_window, columns=("ID", "Title", "Author", "Year", "ISBN", "Issued To", "Issue Date"), show='headings')
    tree.pack()

    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Year", text="Year")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Issued To", text="Issued To")
    tree.heading("Issue Date", text="Issue Date")

    c.execute("SELECT * FROM books")
    rows = c.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)

def logout(admin_window):
    admin_window.destroy()
    login_window.deiconify()

# Login UI
login_window = tk.Tk()
login_window.title("Library Management System")
login_window.configure(bg='black')

tk.Label(login_window, text="Username", bg='black', fg='white').pack(pady=5)
entry_username = tk.Entry(login_window)
entry_username.pack(pady=5)

tk.Label(login_window, text="Password", bg='black', fg='white').pack(pady=5)
entry_password = tk.Entry(login_window, show="*")
entry_password.pack(pady=5)

tk.Button(login_window, text="Login", command=login).pack(pady=10)

login_window.mainloop()
