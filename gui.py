import mysql.connector
import ttkbootstrap as tb
from tkinter import *
from tkinter import ttk, messagebox
import datetime

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
        
        # Enable buttons after data is loaded
        delete_btn.config(state=NORMAL)
        edit_btn.config(state=NORMAL)
    
    def delete_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Information", "Please select a record to delete")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            return
            
        # Get the table name
        table_map = {
            "Authors": "authors",
            "Books": "books",
            "Users": "users",
            "Issued Books": "issued_books"
        }
        selected_table = table_map[combo.get()]
        
        # Get primary key column (first column) and value
        columns = tree.cget("columns")
        primary_key_col = columns[0]
        values = tree.item(selected_item, 'values')
        primary_key_val = values[0]
        
        try:
            cursor.execute(f"DELETE FROM {selected_table} WHERE {primary_key_col} = %s", (primary_key_val,))
            db_connection.commit()
            messagebox.showinfo("Success", "Record deleted successfully")
            fetch_and_display()  # Refresh the view
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete record: {err}")
    
    def edit_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Information", "Please select a record to edit")
            return
            
        # Get selected record data
        values = tree.item(selected_item, 'values')
        
        # Get column names
        columns = tree.cget("columns")
        
        # Get table name
        table_map = {
            "Authors": "authors",
            "Books": "books",
            "Users": "users",
            "Issued Books": "issued_books"
        }
        selected_table = table_map[combo.get()]
        
        # Create edit window
        edit_win = Toplevel(query_win)
        edit_win.title(f"Edit {combo.get()} Record")
        edit_win.geometry("500x500")
        
        # Create entry widgets for each column
        entries = {}
        for i, col in enumerate(columns):
            Label(edit_win, text=f"{col.replace('_', ' ').title()}:").grid(row=i, column=0, padx=10, pady=5, sticky=W)
            entry = Entry(edit_win, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, values[i] if values[i] is not None else "")
            entries[col] = entry
        
        def save_changes():
            try:
                # Get primary key column (usually the first column)
                primary_key_col = columns[0]
                primary_key_val = values[0]
                
                # Build UPDATE query
                set_clause = ", ".join([f"{col} = %s" for col in columns])
                update_values = [entries[col].get() for col in columns]
                
                # Add WHERE clause value
                where_clause = f"{primary_key_col} = %s"
                update_values.append(primary_key_val)
                
                # Execute update
                cursor.execute(
                    f"UPDATE {selected_table} SET {set_clause} WHERE {where_clause}", 
                    update_values
                )
                db_connection.commit()
                messagebox.showinfo("Success", "Record updated successfully")
                edit_win.destroy()
                fetch_and_display()  # Refresh the view
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update record: {err}")
        
        # Save button
        Button(edit_win, text="Save Changes", command=save_changes).grid(
            row=len(columns)+1, column=0, columnspan=2, pady=15
        )

    query_win = Toplevel(root)
    query_win.title("Query Information")
    query_win.geometry("700x400")

    Label(query_win, text="Select Category:", font=("Arial", 14)).pack(pady=5)
    combo = ttk.Combobox(query_win, values=["Authors", "Books", "Users", "Issued Books"], state="readonly")
    combo.current(0)  # Set default selection
    combo.pack(pady=5)

    # Button frame
    btn_frame = Frame(query_win)
    btn_frame.pack(pady=5)
    
    Button(btn_frame, text="Fetch Data", command=fetch_and_display).grid(row=0, column=0, padx=10)
    delete_btn = Button(btn_frame, text="Delete Selected", command=delete_record, state=DISABLED)
    delete_btn.grid(row=0, column=1, padx=10)
    edit_btn = Button(btn_frame, text="Edit Selected", command=edit_record, state=DISABLED)
    edit_btn.grid(row=0, column=2, padx=10)

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
    def search_book():
        book_no = entry_book_no.get()
        if not book_no:
            messagebox.showinfo("Information", "Please enter a book number.")
            return
            
        cursor.execute("SELECT book_name FROM books WHERE book_no = %s", (book_no,))
        book_name_result = cursor.fetchone()
        
        if not book_name_result:
            messagebox.showinfo("Information", "No book found with the provided book number.")
            return
            
        book_name_var.set(book_name_result[0])
        
        cursor.execute("SELECT author_id FROM books WHERE book_no = %s", (book_no,))
        author_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT author_name FROM authors WHERE author_id = %s", (author_id,))
        author_result = cursor.fetchone()
        
        if author_result:
            book_author_var.set(author_result[0])
            submit_btn['state'] = 'normal'
        else:
            book_author_var.set("Unknown Author")
            messagebox.showinfo("Warning", "Author information not found, but you can proceed.")
            submit_btn['state'] = 'normal'
    
    def submit():
        book_no = entry_book_no.get()
        book_name = book_name_var.get()
        book_author = book_author_var.get()
        student_id = entry_student_id.get()
        status = 1
        issue_date = entry_issue_date.get()
        # Validate student ID exists
        cursor.execute("SELECT id FROM users WHERE id = %s", (student_id,))
        student_exists = cursor.fetchone()
        if not student_exists:
            messagebox.showerror("Error", "Student ID does not exist in the database.")
            return

        # Validate date format
        try:
            datetime.datetime.strptime(issue_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD format.")
            return
        
        if book_no and book_name and book_author and student_id and issue_date:
            cursor.execute("INSERT INTO issued_books (book_no, book_name, book_author, student_id, status, issue_date) VALUES (%s, %s, %s, %s, %s, %s)",
                           (book_no, book_name, book_author, student_id, status, issue_date))
            db_connection.commit()
            messagebox.showinfo("Success", "Book issued successfully!")
            issue_win.destroy()
        else:
            messagebox.showinfo("Information", "Please fill all fields.")

    issue_win = Toplevel(root)
    issue_win.title("Issue Book")
    issue_win.geometry("400x500")

    # Book Number
    Label(issue_win, text="Enter Book Number:").pack(pady=5)
    entry_book_no = Entry(issue_win)
    entry_book_no.pack(pady=5)
    Button(issue_win, text="Search Book", command=search_book).pack(pady=5)
    
    # Book Name (display only)
    Label(issue_win, text="Book Name:").pack(pady=5)
    book_name_var = StringVar()
    Label(issue_win, textvariable=book_name_var, bg="white", width=30).pack(pady=5)
    
    # Book Author (display only)
    Label(issue_win, text="Book Author:").pack(pady=5)
    book_author_var = StringVar()
    Label(issue_win, textvariable=book_author_var, bg="white", width=30).pack(pady=5)
    
    # Student ID
    Label(issue_win, text="Enter Student ID:").pack(pady=5)
    entry_student_id = Entry(issue_win)
    entry_student_id.pack(pady=5)

    # Issue Date
    Label(issue_win, text="Enter Issue Date (YYYY-MM-DD):").pack(pady=5)
    entry_issue_date = Entry(issue_win)
    entry_issue_date.pack(pady=5)

    # Submit button (disabled until book is found)
    submit_btn = Button(issue_win, text="Submit", command=submit, state='disabled')
    submit_btn.pack(pady=10)

# Function to Delete Information
def delete_information():
    def submit():
        selected = combo.get()
        value = entry.get()
        
        if selected and value:
            if selected == "User":
                cursor.execute("DELETE FROM users WHERE id = %s", (value,))
            elif selected == "Book":
                cursor.execute("DELETE FROM books WHERE book_no = %s", (value,))
            elif selected == "Author":
                cursor.execute("DELETE FROM authors WHERE author_name = %s", (value,))
                
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
    field_label = Label(delete_win, text="Enter Student Id:")
    field_label.pack(pady=5)
    
    entry = Entry(delete_win, width=30)
    entry.pack(pady=5)
    
    # Update the label when selection changes
    def update_field_label(event):
        selected = combo.get()
        if selected == "User":
            field_label.config(text="Enter Student Id:")
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
            cursor.execute("INSERT INTO authors (author_name) VALUES (%s)", 
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
# Function to Query Backup Tables
def query_backup():
    
    def fetch_and_display():
        backup_table_map = {
            "Authors Backup": "authors_backup",
            "Books Backup": "books_backup",
            "Users Backup": "users_backup",
            "Issued Books Backup": "issued_books_backup"
        }
        
        selected_backup = backup_table_map[combo.get()]
        
        # Check if the backup table exists
        try:
            cursor.execute(f"SHOW TABLES LIKE '{selected_backup}'")
            if not cursor.fetchone():
                messagebox.showinfo("Information", f"Backup table '{selected_backup}' does not exist.")
                return
                
            cursor.execute(f"SELECT * FROM {selected_backup}")
            results = cursor.fetchall()
            
            # Get column names
            cursor.execute(f"SHOW COLUMNS FROM {selected_backup}")
            columns = [column[0] for column in cursor.fetchall()]
            
            # Configure columns in treeview
            tree["columns"] = columns
            
            # Clear old data
            for row in tree.get_children():
                tree.delete(row)
            
            # Set headers
            for col in columns:
                tree.heading(col, text=col.replace('_', ' ').title())
                tree.column(col, width=100)
            
            # Insert data
            for row in results:
                tree.insert("", END, values=row)
            
            # Enable buttons after data is loaded
            clear_btn.config(state=NORMAL)
            edit_btn.config(state=NORMAL)
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error accessing backup table: {err}")
    
    def clear_all():
        backup_table_map = {
            "Authors Backup": "authors_backup",
            "Books Backup": "books_backup",
            "Users Backup": "users_backup",
            "Issued Books Backup": "issued_books_backup"
        }
        
        selected_backup = backup_table_map[combo.get()]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to clear all records from {selected_backup}?"):
            try:
                cursor.execute(f"DELETE FROM {selected_backup}")
                db_connection.commit()
                messagebox.showinfo("Success", f"All records deleted from {selected_backup}")
                fetch_and_display()  # Refresh the display
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to clear table: {err}")
    
    def edit_record():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showinfo("Information", "Please select a record to edit")
            return
        
        # Get selected record data
        values = tree.item(selected_item, 'values')
        
        # Get column names
        columns = tree.cget("columns")
        
        # Get table name
        backup_table_map = {
            "Authors Backup": "authors_backup",
            "Books Backup": "books_backup",
            "Users Backup": "users_backup",
            "Issued Books Backup": "issued_books_backup"
        }
        selected_backup = backup_table_map[combo.get()]
        
        # Create edit window
        edit_win = Toplevel(backup_win)
        edit_win.title(f"Edit {combo.get()} Record")
        edit_win.geometry("500x500")
        
        # Create entry widgets for each column
        entries = {}
        for i, col in enumerate(columns):
            Label(edit_win, text=f"{col.replace('_', ' ').title()}:").grid(row=i, column=0, padx=10, pady=5, sticky=W)
            entry = Entry(edit_win, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry.insert(0, values[i] if values[i] is not None else "")
            entries[col] = entry
        
        def save_changes():
            try:
                # Get primary key column (usually the first column)
                primary_key_col = columns[0]
                primary_key_val = values[0]
                
                # Build UPDATE query
                set_clause = ", ".join([f"{col} = %s" for col in columns])
                update_values = [entries[col].get() for col in columns]
                
                # Add WHERE clause value
                where_clause = f"{primary_key_col} = %s"
                update_values.append(primary_key_val)
                
                # Execute update
                cursor.execute(
                    f"UPDATE {selected_backup} SET {set_clause} WHERE {where_clause}", 
                    update_values
                )
                db_connection.commit()
                messagebox.showinfo("Success", "Record updated successfully")
                edit_win.destroy()
                fetch_and_display()  # Refresh the view
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update record: {err}")
        
        # Save button
        Button(edit_win, text="Save Changes", command=save_changes).grid(
            row=len(columns)+1, column=0, columnspan=2, pady=15
        )

    backup_win = Toplevel(root)
    backup_win.title("Query Backup Tables")
    backup_win.geometry("800x500")

    Label(backup_win, text="Select Backup Table:", font=("Arial", 14)).pack(pady=5)
    combo = ttk.Combobox(backup_win, values=["Authors Backup", "Books Backup", "Users Backup", "Issued Books Backup"], state="readonly")
    combo.current(0)
    combo.pack(pady=5)

    # Button frame
    btn_frame = Frame(backup_win)
    btn_frame.pack(pady=5)
    
    Button(btn_frame, text="Fetch Backup Data", command=fetch_and_display).grid(row=0, column=0, padx=10)
    clear_btn = Button(btn_frame, text="Clear All Records", command=clear_all, state=DISABLED)
    clear_btn.grid(row=0, column=1, padx=10)
    edit_btn = Button(btn_frame, text="Edit Selected Record", command=edit_record, state=DISABLED)
    edit_btn.grid(row=0, column=2, padx=10)

    # Create treeview
    tree = ttk.Treeview(backup_win, show="headings")
    tree.pack(expand=True, fill=BOTH, padx=10, pady=10)
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

# Add backup query button
Button(button_frame, text="Query Backups", width=20, command=query_backup).grid(row=2, column=0, padx=15, pady=15)
root.mainloop()
