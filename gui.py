import mysql.connector
import ttkbootstrap as tb
from tkinter import *
from tkinter import ttk, messagebox
import datetime
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="prasanga",
    database="lms"
)
cursor = db_connection.cursor()

# Main App 
root = tb.Window(themename="cosmo")  
root.title("Library Management System")
root.geometry("1100x750") 


style = tb.Style()
style.configure("TButton", font=("Helvetica", 10))
style.configure("TLabel", font=("Helvetica", 10))
style.configure("Accent.TButton", background="#0078D7")


header_frame = Frame(root, bg="#0078D7", height=70)
header_frame.pack(fill=X)
header_frame.pack_propagate(False)

title_label = Label(header_frame, text="Library Management System", 
                   font=("Helvetica", 21, "bold"), bg="#0078D7", fg="white")
title_label.pack(pady=5)



notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True, padx=15, pady=15)


def create_tab_frame(parent):
    frame = ttk.Frame(parent, padding=15)
    return frame

query_tab = create_tab_frame(notebook)
add_tab = create_tab_frame(notebook)
issue_tab = create_tab_frame(notebook)
backup_tab = create_tab_frame(notebook)

notebook.add(query_tab, text=" 🔍 Query Information ")
notebook.add(add_tab, text=" ➕ Add Records ")
notebook.add(issue_tab, text=" 📚 Issue Books ")
notebook.add(backup_tab, text=" 💾 Backups ")

add_notebook = ttk.Notebook(add_tab)
add_notebook.pack(fill=BOTH, expand=True)

user_tab = ttk.Frame(add_notebook)
author_tab = ttk.Frame(add_notebook)
book_tab = ttk.Frame(add_notebook)

add_notebook.add(user_tab, text="Add User")
add_notebook.add(author_tab, text="Add Author")
add_notebook.add(book_tab, text="Add Book")

#QUERY TAB
query_frame = ttk.Frame(query_tab)
query_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

Label(query_frame, text="Select Category:", font=("Arial", 14)).pack(pady=5)
query_combo = ttk.Combobox(query_frame, values=["Authors", "Books", "Users", "Issued Books"], state="readonly")
query_combo.current(0)
query_combo.pack(pady=5)

query_btn_frame = Frame(query_frame)
query_btn_frame.pack(pady=5)


query_tree = ttk.Treeview(query_frame, show="headings")
query_tree.pack(expand=True, fill=BOTH, padx=5, pady=5)

query_scrollbar = ttk.Scrollbar(query_tree, orient="vertical", command=query_tree.yview)
query_tree.configure(yscrollcommand=query_scrollbar.set)
query_scrollbar.pack(side=RIGHT, fill=Y)

def fetch_and_display():
    table_map = {
        "Authors": "authors",
        "Books": "books",
        "Users": "users",
        "Issued Books": "issued_books"
    }
    
    selected_table = table_map[query_combo.get()]
    

    if selected_table == "issued_books":
        cursor.execute("""
            SELECT i.*, b.book_name 
            FROM issued_books i
            LEFT JOIN books b ON i.book_id = b.book_id
        """)
        results = cursor.fetchall()
        

        cursor.execute(f"SHOW COLUMNS FROM {selected_table}")
        columns = [column[0] for column in cursor.fetchall()]

        columns.append("book_name")
    else:
        cursor.execute(f"SELECT * FROM {selected_table}")
        results = cursor.fetchall()
        
        cursor.execute(f"SHOW COLUMNS FROM {selected_table}")
        columns = [column[0] for column in cursor.fetchall()]
    
    query_tree["columns"] = columns
    

    for row in query_tree.get_children():
        query_tree.delete(row)
    

    for i, col in enumerate(columns):
        query_tree.heading(col, text=col.replace('_', ' ').title(), anchor=CENTER)
        query_tree.column(col, width=100, anchor=CENTER)  
    
    for row in results:
        query_tree.insert("", END, values=row)
    
    delete_btn.config(state=NORMAL)
    edit_btn.config(state=NORMAL)

def edit_record():
    selected_item = query_tree.selection()
    if not selected_item:
        messagebox.showinfo("Information", "Please select a record to edit")
        return
        
    values = query_tree.item(selected_item, 'values')
    columns = query_tree.cget("columns")
    
    table_map = {
        "Authors": "authors",
        "Books": "books",
        "Users": "users",
        "Issued Books": "issued_books"
    }
    selected_table = table_map[query_combo.get()]
    

    edit_frame = Frame(query_frame, bd=2, relief=RIDGE)
    edit_frame.pack(fill=X, padx=10, pady=10)
    
    Label(edit_frame, text=f"Edit {query_combo.get()} Record", font=("Arial", 12, "bold")).pack(pady=5)
    
    entries = {}
    entry_frame = Frame(edit_frame)
    entry_frame.pack(fill=X, padx=10)
    

    is_issued_books = selected_table == "issued_books"
    update_columns = columns if not is_issued_books else [col for col in columns if col != "book_name"]
    
    for i, col in enumerate(columns):
        row_frame = Frame(entry_frame)
        row_frame.pack(fill=X, pady=2)
        
        Label(row_frame, text=f"{col.replace('_', ' ').title()}:", width=15).pack(side=LEFT)
        
        if is_issued_books and col == "book_name":
            entry = Entry(row_frame, width=30, state="readonly", readonlybackground="white")
            entry.pack(side=LEFT, fill=X, expand=True, padx=5)
            entry.config(state=NORMAL)  
            entry.insert(0, values[i] if values[i] is not None else "")
            entry.config(state="readonly")  
        else:
            entry = Entry(row_frame, width=30)
            entry.pack(side=LEFT, fill=X, expand=True, padx=5)
            entry.insert(0, values[i] if values[i] is not None else "")
        
        entries[col] = entry
    
    def save_changes():
        try:
            primary_key_col = update_columns[0]  
            primary_key_val = values[0]
            
            set_clause = ", ".join([f"{col} = %s" for col in update_columns])
            update_values = []
            

            for col in update_columns:
                update_values.append(entries[col].get())
            
            where_clause = f"{primary_key_col} = %s"
            update_values.append(primary_key_val)
            
            cursor.execute(
                f"UPDATE {selected_table} SET {set_clause} WHERE {where_clause}", 
                update_values
            )
            db_connection.commit()
            messagebox.showinfo("Success", "Record updated successfully")
            edit_frame.destroy()
            fetch_and_display()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update record: {err}")
    
    def cancel_edit():
        edit_frame.destroy()
    
    btn_frame = Frame(edit_frame)
    btn_frame.pack(pady=10)
    Button(btn_frame, text="Save Changes", command=save_changes).pack(side=LEFT, padx=5)
    Button(btn_frame, text="Cancel", command=cancel_edit).pack(side=LEFT, padx=5)

def delete_record():
    selected_item = query_tree.selection()
    if not selected_item:
        messagebox.showinfo("Information", "Please select a record to delete")
        return
    
    if not messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
        return
        
    table_map = {
        "Authors": "authors",
        "Books": "books",
        "Users": "users",
        "Issued Books": "issued_books"
    }
    selected_table = table_map[query_combo.get()]
    
    columns = query_tree.cget("columns")
    primary_key_col = columns[0]
    values = query_tree.item(selected_item, 'values')
    primary_key_val = values[0]
    
    try:
        cursor.execute(f"DELETE FROM {selected_table} WHERE {primary_key_col} = %s", (primary_key_val,))
        db_connection.commit()
        messagebox.showinfo("Success", "Record deleted successfully")
        fetch_and_display()  
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to delete record: {err}")



Button(query_btn_frame, text="Fetch Data", command=fetch_and_display).grid(row=0, column=0, padx=10)
delete_btn = Button(query_btn_frame, text="Delete Selected", command=delete_record, state=DISABLED)
delete_btn.grid(row=0, column=1, padx=10)
edit_btn = Button(query_btn_frame, text="Edit Selected", command=edit_record, state=DISABLED)
edit_btn.grid(row=0, column=2, padx=10)

# ADD USER TAB
user_frame = ttk.Frame(user_tab)
user_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

Label(user_frame, text="Add New User", font=("Arial", 14, "bold")).pack(pady=10)

user_fields_frame = Frame(user_frame)
user_fields_frame.pack(fill=X, padx=20)

Label(user_fields_frame, text="User ID:").grid(row=0, column=0, sticky=W, pady=5)
entry_user_id = Entry(user_fields_frame, width=30)
entry_user_id.grid(row=0, column=1, pady=5, padx=5)

Label(user_fields_frame, text="User Name:").grid(row=1, column=0, sticky=W, pady=5)
entry_user_name = Entry(user_fields_frame, width=30)
entry_user_name.grid(row=1, column=1, pady=5, padx=5)

Label(user_fields_frame, text="Email:").grid(row=2, column=0, sticky=W, pady=5)
entry_user_email = Entry(user_fields_frame, width=30)
entry_user_email.grid(row=2, column=1, pady=5, padx=5)

Label(user_fields_frame, text="Password:").grid(row=3, column=0, sticky=W, pady=5)
entry_user_pass = Entry(user_fields_frame, show="*", width=30)
entry_user_pass.grid(row=3, column=1, pady=5, padx=5)

Label(user_fields_frame, text="Mobile:").grid(row=4, column=0, sticky=W, pady=5)
entry_user_mobile = Entry(user_fields_frame, width=30)
entry_user_mobile.grid(row=4, column=1, pady=5, padx=5)

Label(user_fields_frame, text="Address:").grid(row=5, column=0, sticky=W, pady=5)
entry_user_address = Entry(user_fields_frame, width=30)
entry_user_address.grid(row=5, column=1, pady=5, padx=5)

def submit_user():
    id, name, email, password, mobile, address = entry_user_id.get(), entry_user_name.get(), entry_user_email.get(), entry_user_pass.get(), entry_user_mobile.get(), entry_user_address.get()
    if name and email and password and mobile and address:
        cursor.execute("INSERT INTO users (id,name, email, password, mobile, address) VALUES (%s, %s, %s, %s, %s,%s)", 
                      (id, name, email, password, mobile, address))
        db_connection.commit()
        messagebox.showinfo("Success", "User added successfully!")

        entry_user_id.delete(0, END)
        entry_user_name.delete(0, END)
        entry_user_email.delete(0, END)
        entry_user_pass.delete(0, END)
        entry_user_mobile.delete(0, END)
        entry_user_address.delete(0, END)
    else:
        messagebox.showinfo("Error", "All fields are required")

Button(user_frame, text="Add User", command=submit_user).pack(pady=10)

#ADD AUTHOR TAB
author_frame = ttk.Frame(author_tab)
author_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

Label(author_frame, text="Add New Author", font=("Arial", 14, "bold")).pack(pady=10)

author_fields_frame = Frame(author_frame)
author_fields_frame.pack(fill=X, padx=20)

Label(author_fields_frame, text="Author ID:").grid(row=0, column=0, sticky=W, pady=5)
entry_author_id = Entry(author_fields_frame, width=30)
entry_author_id.grid(row=0, column=1, pady=5, padx=5)

Label(author_fields_frame, text="Author Name:").grid(row=1, column=0, sticky=W, pady=5)
entry_author_name = Entry(author_fields_frame, width=30)
entry_author_name.grid(row=1, column=1, pady=5, padx=5)

def submit_author():
    author_id = entry_author_id.get()
    name = entry_author_name.get()
    if name:
        cursor.execute("INSERT INTO authors (author_id,author_name) VALUES (%s,%s)", 
                      (author_id, name))
        db_connection.commit()
        messagebox.showinfo("Success", "Author added successfully!")
        entry_author_id.delete(0, END)
        entry_author_name.delete(0, END)
    else:
        messagebox.showinfo("Error", "Author name is required")

Button(author_frame, text="Add Author", command=submit_author).pack(pady=10)

# ADD BOOK TAB
book_frame = ttk.Frame(book_tab)
book_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

Label(book_frame, text="Add New Book", font=("Arial", 14, "bold")).pack(pady=10)

book_fields_frame = Frame(book_frame)
book_fields_frame.pack(fill=X, padx=20)

Label(book_fields_frame, text="Book ID:").grid(row=0, column=0, sticky=W, pady=5)
entry_book_id = Entry(book_fields_frame, width=30)
entry_book_id.grid(row=0, column=1, pady=5, padx=5)

Label(book_fields_frame, text="Book Name:").grid(row=1, column=0, sticky=W, pady=5)
entry_book_title = Entry(book_fields_frame, width=30)
entry_book_title.grid(row=1, column=1, pady=5, padx=5)

Label(book_fields_frame, text="Author ID:").grid(row=2, column=0, sticky=W, pady=5)
entry_book_author_id = Entry(book_fields_frame, width=30)
entry_book_author_id.grid(row=2, column=1, pady=5, padx=5)

Label(book_fields_frame, text="Category ID:").grid(row=3, column=0, sticky=W, pady=5)
entry_book_cat = Entry(book_fields_frame, width=30)
entry_book_cat.grid(row=3, column=1, pady=5, padx=5)

Label(book_fields_frame, text="Book Number:").grid(row=4, column=0, sticky=W, pady=5)
entry_book_num = Entry(book_fields_frame, width=30)
entry_book_num.grid(row=4, column=1, pady=5, padx=5)

Label(book_fields_frame, text="Book Price:").grid(row=5, column=0, sticky=W, pady=5)
entry_book_price = Entry(book_fields_frame, width=30)
entry_book_price.grid(row=5, column=1, pady=5, padx=5)

def submit_book():
    book_id = entry_book_id.get()
    title = entry_book_title.get()
    author_id = entry_book_author_id.get()
    cat_id = entry_book_cat.get()
    book_num = entry_book_num.get()
    price = entry_book_price.get()
    
    if title and author_id and cat_id:
        cursor.execute("INSERT INTO books (book_id,book_name,author_id,cat_id,book_no,book_price) VALUES (%s,%s,%s,%s,%s,%s)", 
                      (book_id, title, author_id, cat_id, book_num, price))
        db_connection.commit()
        messagebox.showinfo("Success", "Book added successfully!")
        entry_book_id.delete(0, END)
        entry_book_title.delete(0, END)
        entry_book_author_id.delete(0, END)
        entry_book_cat.delete(0, END)
        entry_book_num.delete(0, END)
        entry_book_price.delete(0, END)
    else:
        messagebox.showinfo("Error", "Missing fields. Please fill all required fields.")

Button(book_frame, text="Add Book", command=submit_book).pack(pady=10)

# ISSUE BOOK TAB
issue_frame = ttk.Frame(issue_tab)
issue_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

Label(issue_frame, text="Issue Book", font=("Arial", 14, "bold")).pack(pady=10)

issue_fields_frame = Frame(issue_frame)
issue_fields_frame.pack(fill=X, padx=20)

Label(issue_fields_frame, text="Book ID:").grid(row=0, column=0, sticky=W, pady=5)
entry_issue_book_id = Entry(issue_fields_frame, width=30)
entry_issue_book_id.grid(row=0, column=1, pady=5, padx=5)

Label(issue_fields_frame, text="Book Name:").grid(row=1, column=0, sticky=W, pady=5)
book_name_var = StringVar()
Label(issue_fields_frame, textvariable=book_name_var, bg="white", width=30, relief=SUNKEN, anchor=W).grid(row=1, column=1, pady=5, padx=5)

Label(issue_fields_frame, text="Book Author:").grid(row=2, column=0, sticky=W, pady=5)
book_author_var = StringVar()
Label(issue_fields_frame, textvariable=book_author_var, bg="white", width=30, relief=SUNKEN, anchor=W).grid(row=2, column=1, pady=5, padx=5)

Label(issue_fields_frame, text="Student ID:").grid(row=3, column=0, sticky=W, pady=5)
entry_issue_student_id = Entry(issue_fields_frame, width=30)
entry_issue_student_id.grid(row=3, column=1, pady=5, padx=5)

Label(issue_fields_frame, text="Issue Date (YYYY-MM-DD):").grid(row=4, column=0, sticky=W, pady=5)
entry_issue_date = Entry(issue_fields_frame, width=30)
entry_issue_date.grid(row=4, column=1, pady=5, padx=5)
entry_issue_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

def search_book():
    book_id = entry_issue_book_id.get()
    if not book_id:
        messagebox.showinfo("Information", "Please enter a book ID.")
        return
        
    cursor.execute("SELECT book_name FROM books WHERE book_id = %s", (book_id,))
    book_name_result = cursor.fetchone()
    
    if not book_name_result:
        messagebox.showinfo("Information", "No book found with the provided book ID.")
        return
        
    book_name_var.set(book_name_result[0])
    
    cursor.execute("SELECT author_id FROM books WHERE book_id = %s", (book_id,))
    author_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT author_name FROM authors WHERE author_id = %s", (author_id,))
    author_result = cursor.fetchone()
    
    if author_result:
        book_author_var.set(author_result[0])
        issue_btn['state'] = 'normal'
    else:
        book_author_var.set("Unknown Author")
        messagebox.showinfo("Warning", "Author information not found, but you can proceed.")
        issue_btn['state'] = 'normal'

def submit_issue():
    book_id = entry_issue_book_id.get()
    book_name = book_name_var.get()
    book_author = book_author_var.get()
    student_id = entry_issue_student_id.get()
    status = 1
    issue_date = entry_issue_date.get()
    
    # Check if student exists
    cursor.execute("SELECT id FROM users WHERE id = %s", (student_id,))
    student_exists = cursor.fetchone()
    if not student_exists:
        messagebox.showerror("Error", "Student ID does not exist in the database.")
        return

    # Check if book is already issued to any student
    cursor.execute("SELECT * FROM issued_books WHERE book_id = %s AND status = 1", (book_id,))
    already_issued = cursor.fetchone()
    if already_issued:
        messagebox.showerror("Duplication Error", "This book is already issued.")
        return

    try:
        datetime.datetime.strptime(issue_date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD format.")
        return
    
    if book_id and student_id and issue_date:
        cursor.execute("INSERT INTO issued_books (book_id,student_id, status, issue_date) VALUES (%s, %s, %s, %s)",
                       (book_id, student_id, status, issue_date))
        db_connection.commit()
        messagebox.showinfo("Success", "Book issued successfully!")
        entry_issue_book_id.delete(0, END)
        entry_issue_student_id.delete(0, END)
        book_name_var.set("")
        book_author_var.set("")
        issue_btn['state'] = 'disabled'
    else:
        messagebox.showinfo("Information", "Please fill all fields.")

Button(issue_fields_frame, text="Search Book", command=search_book).grid(row=0, column=2, padx=5)
issue_btn = Button(issue_frame, text="Issue Book", command=submit_issue, state='disabled')
issue_btn.pack(pady=10)

#BACKUP TAB
backup_frame = ttk.Frame(backup_tab)
backup_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

Label(backup_frame, text="Query Backup Tables", font=("Arial", 14, "bold")).pack(pady=10)

backup_combo = ttk.Combobox(backup_frame, values=["Authors Backup", "Books Backup", "Users Backup", "Issued Books Backup"], state="readonly")
backup_combo.current(0)
backup_combo.pack(pady=5)

backup_btn_frame = Frame(backup_frame)
backup_btn_frame.pack(pady=5)

backup_tree = ttk.Treeview(backup_frame, show="headings")
backup_tree.pack(expand=True, fill=BOTH, padx=5, pady=5)

backup_scrollbar = ttk.Scrollbar(backup_tree, orient="vertical", command=backup_tree.yview)
backup_tree.configure(yscrollcommand=backup_scrollbar.set)
backup_scrollbar.pack(side=RIGHT, fill=Y)

def fetch_backup():
    backup_table_map = {
        "Authors Backup": "authors_backup",
        "Books Backup": "books_backup",
        "Users Backup": "users_backup",
        "Issued Books Backup": "issued_books_backup"
    }
    
    selected_backup = backup_table_map[backup_combo.get()]
    
    # Check if the backup table exists
    try:
        cursor.execute(f"SHOW TABLES LIKE '{selected_backup}'")
        if not cursor.fetchone():
            messagebox.showinfo("Information", f"Backup table '{selected_backup}' does not exist.")
            return
            
        cursor.execute(f"SELECT * FROM {selected_backup}")
        results = cursor.fetchall()
        
        cursor.execute(f"SHOW COLUMNS FROM {selected_backup}")
        columns = [column[0] for column in cursor.fetchall()]
        
        backup_tree["columns"] = columns
        
        for row in backup_tree.get_children():
            backup_tree.delete(row)
        
        for col in columns:
            backup_tree.heading(col, text=col.replace('_', ' ').title())
            backup_tree.column(col, width=100)
        
        for row in results:
            backup_tree.insert("", END, values=row)
        
        clear_backup_btn.config(state=NORMAL)
        edit_backup_btn.config(state=NORMAL)
            
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error accessing backup table: {err}")

def clear_backup():
    backup_table_map = {
        "Authors Backup": "authors_backup",
        "Books Backup": "books_backup",
        "Users Backup": "users_backup",
        "Issued Books Backup": "issued_books_backup"
    }
    
    selected_backup = backup_table_map[backup_combo.get()]
    
    if messagebox.askyesno("Confirm", f"Are you sure you want to clear all records from {selected_backup}?"):
        try:
            cursor.execute(f"DELETE FROM {selected_backup}")
            db_connection.commit()
            messagebox.showinfo("Success", f"All records deleted from {selected_backup}")
            fetch_backup() 
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to clear table: {err}")

def edit_backup():
    selected_item = backup_tree.selection()
    if not selected_item:
        messagebox.showinfo("Information", "Please select a record to edit")
        return
    
    values = backup_tree.item(selected_item, 'values')
    columns = backup_tree.cget("columns")
    
    backup_table_map = {
        "Authors Backup": "authors_backup",
        "Books Backup": "books_backup",
        "Users Backup": "users_backup",
        "Issued Books Backup": "issued_books_backup"
    }
    selected_backup = backup_table_map[backup_combo.get()]
    
    # Create edit panel
    edit_backup_frame = Frame(backup_frame, bd=2, relief=RIDGE)
    edit_backup_frame.pack(fill=X, padx=10, pady=10)
    
    Label(edit_backup_frame, text=f"Edit {backup_combo.get()} Record", font=("Arial", 12, "bold")).pack(pady=5)
    
    entries = {}
    entry_backup_frame = Frame(edit_backup_frame)
    entry_backup_frame.pack(fill=X, padx=10)
    
    for i, col in enumerate(columns):
        row_frame = Frame(entry_backup_frame)
        row_frame.pack(fill=X, pady=2)
        
        Label(row_frame, text=f"{col.replace('_', ' ').title()}:", width=15).pack(side=LEFT)
        entry = Entry(row_frame, width=30)
        entry.pack(side=LEFT, fill=X, expand=True, padx=5)
        entry.insert(0, values[i] if values[i] is not None else "")
        entries[col] = entry
    
    def save_changes():
        try:
            primary_key_col = columns[0]
            primary_key_val = values[0]
            
            set_clause = ", ".join([f"{col} = %s" for col in columns])
            update_values = [entries[col].get() for col in columns]
            
            where_clause = f"{primary_key_col} = %s"
            update_values.append(primary_key_val)
            
            cursor.execute(
                f"UPDATE {selected_backup} SET {set_clause} WHERE {where_clause}", 
                update_values
            )
            db_connection.commit()
            messagebox.showinfo("Success", "Record updated successfully")
            edit_backup_frame.destroy()
            fetch_backup()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to update record: {err}")
    
    def cancel_edit():
        edit_backup_frame.destroy()
    
    btn_frame = Frame(edit_backup_frame)
    btn_frame.pack(pady=10)
    Button(btn_frame, text="Save Changes", command=save_changes).pack(side=LEFT, padx=5)
    Button(btn_frame, text="Cancel", command=cancel_edit).pack(side=LEFT, padx=5)

Button(backup_btn_frame, text="Fetch Backup Data", command=fetch_backup).grid(row=0, column=0, padx=10)
clear_backup_btn = Button(backup_btn_frame, text="Clear All Records", command=clear_backup, state=DISABLED)
clear_backup_btn.grid(row=0, column=1, padx=10)
edit_backup_btn = Button(backup_btn_frame, text="Edit Selected", command=edit_backup, state=DISABLED)
edit_backup_btn.grid(row=0, column=2, padx=10)

Button(root, text="Exit", command=root.quit, bg="#b71c1c", fg="white", width=10).pack(pady=10)

root.mainloop()