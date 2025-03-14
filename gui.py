import mysql.connector
import ttkbootstrap as tb
from tkinter import *
from tkinter import ttk, messagebox

# Database Connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="prasanga",
    database="lms"
)
cursor = db_connection.cursor()

# Main App
root = tb.Window(themename="superhero")
root.title("Library Management System")
root.geometry("900x600")

# Function to Display Query Information in Table
def query_information():
    def fetch_and_display():
        table_map = {
            "Authors": "authors",
            "Books": "books",
            "Users": "users",
            "Issued Books": "issued_books"
        }
        
        selected_table = table_map[combo.get()]
        cursor.execute(f"SELECT * FROM {selected_table}")
        results = cursor.fetchall()
        
        # Get column names for the selected table
        cursor.execute(f"SHOW COLUMNS FROM {selected_table}")
        columns = [column[0] for column in cursor.fetchall()]
        
        # Configure columns in treeview
        tree["columns"] = columns
        
        # Clear old data and headers
        for row in tree.get_children():
            tree.delete(row)
        
        # Set headers based on the table selected
        for i, col in enumerate(columns):
            tree.heading(col, text=col.replace('_', ' ').title())
            tree.column(col, width=100)  # Adjust column width as needed
        
        # Insert new data
        for row in results:
            tree.insert("", END, values=row)

    query_win = Toplevel(root)
    query_win.title("Query Information")
    query_win.geometry("700x400")

    Label(query_win, text="Select Category:", font=("Arial", 14)).pack(pady=5)
    combo = ttk.Combobox(query_win, values=["Authors", "Books", "Users", "Issued Books"], state="readonly")
    combo.current(0)  # Set default selection
    combo.pack(pady=5)

    Button(query_win, text="Fetch Data", command=fetch_and_display).pack(pady=5)

    # Create treeview with dynamic columns
    tree = ttk.Treeview(query_win, show="headings")
    tree.pack(expand=True, fill=BOTH, padx=10, pady=10)
    
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

# Function to Add User
def add_user():
    def submit():
        name, email, password, mobile, address = entry_name.get(), entry_email.get(), entry_pass.get(), entry_mobile.get(), entry_address.get()
        if name and email and password and mobile and address:
            cursor.execute("INSERT INTO users (name, email, password, mobile, address) VALUES (%s, %s, %s, %s, %s)", 
                           (name, email, password, mobile, address))
            db_connection.commit()
            messagebox.showinfo("Success", "User added successfully!")
            add_win.destroy()

    add_win = Toplevel(root)
    add_win.title("Add User")
    add_win.geometry("400x500")

    Label(add_win, text="Enter User Name:").pack(pady=5)
    entry_name = Entry(add_win)
    entry_name.pack(pady=5)

    Label(add_win, text="Enter Email:").pack(pady=5)
    entry_email = Entry(add_win)
    entry_email.pack(pady=5)

    Label(add_win, text="Enter Password:").pack(pady=5)
    entry_pass = Entry(add_win, show="*")
    entry_pass.pack(pady=5)

    Label(add_win, text="Enter Mobile:").pack(pady=5)
    entry_mobile = Entry(add_win)
    entry_mobile.pack(pady=5)

    Label(add_win, text="Enter Address:").pack(pady=5)
    entry_address = Entry(add_win)
    entry_address.pack(pady=5)

    Button(add_win, text="Submit", command=submit).pack(pady=10)

# Function to Issue a Book
def add_issue():
    def submit():
        book_no, book_name, book_author, student_id, status, issue_date = entry_book_no.get(), entry_book_name.get(), entry_book_author.get(), entry_student_id.get(), 1, entry_issue_date.get()
        if book_no and book_name and book_author and student_id and issue_date:
            cursor.execute("INSERT INTO issued_books (book_no, book_name, book_author, student_id, status, issue_date) VALUES (%s, %s, %s, %s, %s, %s)",
                           (book_no, book_name, book_author, student_id, status, issue_date))
            db_connection.commit()
            messagebox.showinfo("Success", "Book issued successfully!")
            issue_win.destroy()

    issue_win = Toplevel(root)
    issue_win.title("Issue Book")
    issue_win.geometry("400x500")

    Label(issue_win, text="Enter Book Number:").pack(pady=5)
    entry_book_no = Entry(issue_win)
    entry_book_no.pack(pady=5)

    Label(issue_win, text="Enter Book Name:").pack(pady=5)
    entry_book_name = Entry(issue_win)
    entry_book_name.pack(pady=5)

    Label(issue_win, text="Enter Book Author:").pack(pady=5)
    entry_book_author = Entry(issue_win)
    entry_book_author.pack(pady=5)

    Label(issue_win, text="Enter Student ID:").pack(pady=5)
    entry_student_id = Entry(issue_win)
    entry_student_id.pack(pady=5)

    Label(issue_win, text="Enter Issue Date (YYYY-MM-DD):").pack(pady=5)
    entry_issue_date = Entry(issue_win)
    entry_issue_date.pack(pady=5)

    Button(issue_win, text="Submit", command=submit).pack(pady=10)

# Function to Delete Information
def delete_information():
    def submit():
        selected = combo.get()
        value = entry.get()
        
        if selected and value:
            if selected == "User":
                cursor.execute("DELETE FROM users WHERE name = %s", (value,))
            elif selected == "Book":
                cursor.execute("DELETE FROM books WHERE book_no = %s", (value,))
            elif selected == "Author":
                cursor.execute("DELETE FROM authors WHERE name = %s", (value,))
                
            rows_affected = cursor.rowcount
            db_connection.commit()
            
            if rows_affected > 0:
                messagebox.showinfo("Success", f"{selected} deleted successfully!")
            else:
                messagebox.showinfo("Information", f"No {selected} found with the provided information.")
            delete_win.destroy()

    delete_win = Toplevel(root)
    delete_win.title("Delete Information")
    delete_win.geometry("400x250")

    Label(delete_win, text="Select Type to Delete:", font=("Arial", 12)).pack(pady=10)
    combo = ttk.Combobox(delete_win, values=["User", "Book", "Author"], state="readonly")
    combo.current(0)  # Default selection
    combo.pack(pady=5)

    # Label that changes based on selection
    field_label = Label(delete_win, text="Enter User Name:")
    field_label.pack(pady=5)
    
    entry = Entry(delete_win, width=30)
    entry.pack(pady=5)
    
    # Update the label when selection changes
    def update_field_label(event):
        selected = combo.get()
        if selected == "User":
            field_label.config(text="Enter User Name:")
        elif selected == "Book":
            field_label.config(text="Enter Book Number:")
        elif selected == "Author":
            field_label.config(text="Enter Author Name:")
    
    combo.bind("<<ComboboxSelected>>", update_field_label)

    Button(delete_win, text="Delete", command=submit).pack(pady=15)

# Main Menu
Label(root, text="Library Management System", font=("Arial", 20, "bold")).pack(pady=20)

button_frame = Frame(root)
button_frame.pack(pady=30)


# Function to Add Author
def add_author():
    def submit():
        name= entry_name.get()
        if name:
            cursor.execute("INSERT INTO authors (name) VALUES (%s)", 
                          (name,))
            db_connection.commit()
            messagebox.showinfo("Success", "Author added successfully!")
            author_win.destroy()

    author_win = Toplevel(root)
    author_win.title("Add Author")
    author_win.geometry("400x300")

    Label(author_win, text="Enter Author Name:").pack(pady=5)
    entry_name = Entry(author_win)
    entry_name.pack(pady=5)

    Button(author_win, text="Submit", command=submit).pack(pady=10)

# Function to Add Book
def add_book():
    def submit():
        title, author_id, isbn, num,price = entry_title.get(), entry_author_id.get(), entry_isbn.get(), entry_num.get(),entry_price.get()
        if title and author_id and isbn:
            cursor.execute("INSERT INTO books (book_name,author_id,cat_id,book_no,book_price) VALUES (%s, %s, %s, %s,%s)", 
                          (title, author_id, isbn,num,price ))
            db_connection.commit()
            messagebox.showinfo("Success", "Book added successfully!")
            book_win.destroy()

    book_win = Toplevel(root)
    book_win.title("Add Book")
    book_win.geometry("500x450")

    Label(book_win, text="Enter Book Name:").pack(pady=5)
    entry_title = Entry(book_win)
    entry_title.pack(pady=5)

    Label(book_win, text="Enter Author ID:").pack(pady=5)
    entry_author_id = Entry(book_win)
    entry_author_id.pack(pady=5)

    Label(book_win, text="Enter Category Id:").pack(pady=5)
    entry_isbn = Entry(book_win)
    entry_isbn.pack(pady=5)

    Label(book_win, text="Enter Book No:").pack(pady=5)
    entry_num = Entry(book_win)
    entry_num.pack(pady=5)

    Label(book_win, text="Enter Book Price:").pack(pady=5)
    entry_price = Entry(book_win)
    entry_price.pack(pady=5)


    Button(book_win, text="Submit", command=submit).pack(pady=10)


Button(button_frame, text="Query Information", width=20, command=query_information).grid(row=0, column=0, padx=15, pady=15)
Button(button_frame, text="Delete Information", width=20, command=delete_information).grid(row=0, column=1, padx=15, pady=15)
Button(button_frame, text="Issue Book", width=20, command=add_issue).grid(row=0, column=2, padx=15, pady=15)

# Second row - Adding entities
Button(button_frame, text="Add User", width=20, command=add_user).grid(row=1, column=0, padx=15, pady=15)
Button(button_frame, text="Add Author", width=20, command=add_author).grid(row=1, column=1, padx=15, pady=15)
Button(button_frame, text="Add Book", width=20, command=add_book).grid(row=1, column=2, padx=15, pady=15)

# Third row - Exit button (centered)
Button(button_frame, text="Exit", width=20, command=root.quit, bg="#b71c1c", fg="white").grid(row=2, column=1, pady=30)

root.mainloop()
