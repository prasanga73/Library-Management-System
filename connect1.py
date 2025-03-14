import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",        
    user="root",       
    password="prasanga",  
    database="lms"    
)

def update_data(cursor):
    pass


def delete_data(cursor):
    while True:
        print(" What do you want to delete? \n")
        print("1. Delete an author")
        print("2. Delete a book")
        print("3. Delete a user")
        print("4. Exit")
        option = int(input("Enter your choice: "))
        if option == 1:
            delete_author(cursor)
        elif option == 2:
            delete_book(cursor)
        elif option == 3:
            delete_user(cursor)
        elif option == 4:
            break
        else:
            print("Invalid choice. Please try again.")
            print("\n")

def delete_author(cursor):
    author_name = input("Enter the name of the author: ")
    cursor.execute("SELECT * FROM authors WHERE author_name = %s", (author_name,))
    results = cursor.fetchall()
    if len(results) == 0:
        print("Author not found.")
        print("\n")
        return
    author_id = results[0][0]
    cursor.execute("DELETE FROM authors WHERE author_id = %s", (author_id,))
    cursor.execute("DELETE FROM books WHERE author_id = %s", (author_id,))
    cursor.execute("DELETE FROM issued_books WHERE book_author = %s", (author_name,))
    db_connection.commit()
    print("Author deleted successfully.")

def delete_book(cursor):
    book_name = input("Enter the name of the book: ")
    cursor.execute("SELECT * FROM books WHERE book_name = %s", (book_name,))
    results = cursor.fetchall()
    if len(results) == 0:
        print("Book not found.")
        print("\n")
        return
    book_no = results[0][0]
    cursor.execute("DELETE FROM books WHERE book_no = %s", (book_no,))
    cursor.execute("DELETE FROM issued_books WHERE book_no = %s", (book_no,))
    db_connection.commit()
    print("Book deleted successfully.")

def delete_user(cursor):
    user_name = input("Enter the name of the user: ")
    cursor.execute("SELECT * FROM users WHERE name = %s", (user_name,))
    results = cursor.fetchall()
    if len(results) == 0:
        print("User not found.")
        print("\n")
        return
    user_id = results[0][0]
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    cursor.execute("DELETE FROM issued_books WHERE student_id = %s", (user_id,))
    db_connection.commit()
    print("User deleted successfully.")

def add_author(cursor):
    author_name = input("Enter the name of the author: ")
    cursor.execute("INSERT INTO authors (author_name) VALUES (%s)", (author_name,))
    db_connection.commit()
    print("Author added successfully.")

def add_book(cursor):
    cursor.execute("SELECT * FROM authors") 
    results = cursor.fetchall()
    for row in results:
        print(row)
    book_name = input("Enter the name of the book: ")
    author_id = int(input("Enter the author id: "))
    cursor.execute("SELECT * FROM authors WHERE author_id = %s", (author_id,))
    results = cursor.fetchall()
    if len(results) == 0:
        print("Author not found.")
        print("\n")
        return
    cursor.execute("SELECT * FROM category")
    results = cursor.fetchall()
    for row in results:
        print   (row) 
    cat_id = int(input("Enter the category id: "))
    book_no = int(input("Enter the book number: "))
    book_price = int(input("Enter the book price: "))
    cursor.execute("INSERT INTO books (book_name,author_id,cat_id,book_no,book_price) VALUES (%s,%s, %s,%s,%s)", (book_name,author_id,cat_id,book_no,book_price,))
    db_connection.commit()
    print("Book added successfully.")

def add_publisher(cursor):
    print("This is a dummy method")


def add_user(cursor):
    user_name = input("Enter the name of the user: ")
    email = input("Enter the email of the user: ")
    password = input("Enter the password of the user: ")
    mobile = input("Enter the mobile number of the user: ")
    address = input("Enter the address of the user: ")
    cursor.execute("INSERT INTO users (name, email, password, mobile, address) VALUES (%s, %s, %s, %s, %s)", (user_name, email, password, mobile, address,))
    db_connection.commit()
    print("User added successfully.")
    


def add_issue(cursor):
    book_name = input("Enter the book name: ")
    cursor.execute("SELECT book_no FROM books WHERE book_name = %s", (book_name,))
    results = cursor.fetchall()
    if len(results) == 0:
        print("Book not found.")
        print("\n")
        return
    book_no = results[0][0]
    cursor.execute("SELECT * FROM authors")
    results = cursor.fetchall()
    for row in results:
        print(row)
    print('\n')
    book_author = input("Enter the book author: ")
    cursor.execute("SELECT id,name FROM users")
    results = cursor.fetchall()
    for row in results:
        print (row)
    student_id = int(input("Enter the student id: "))
    status = 1
    issue_date = input("Enter the issue date: ")
    cursor.execute("INSERT INTO issued_books (book_no, book_name, book_author, student_id,status, issue_date) VALUES (%s, %s, %s, %s, %s,%s)", (book_no, book_name, book_author, student_id,status, issue_date,))
    db_connection.commit()
    print("Book issued successfully.")



def add_return(cursor):
    book_no = int(input("Enter the book number: "))
    book_name = input("Enter the book name: ")
    cursor.execute('DELETE FROM issued_books WHERE book_no = %s AND book_name = %s', (book_no, book_name,))
    db_connection.commit()
    print("Book returned successfully.")


def starting():
    cursor = db_connection.cursor()
    flag = True
    while flag:
        print("Welcome to the Library Management System")
        print("What would you like to do?")
        print("1. Information or query")
        print("2. Add new data")
        print("3. Delete existing data")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 2:
            while True:
                print("1. Add a new author")
                print("2. Add a new book")
                print("3. Add a new publisher")
                print("4. Add a new user")
                print("5. Add a new issue")
                print("6. Add a new return")
                print("7. Exit")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    add_author(cursor)
                elif choice == 2:
                    add_book(cursor)
                elif choice == 3:
                    add_publisher(cursor)
                elif choice == 4:
                    add_user(cursor)
                elif choice == 5:
                    add_issue(cursor)
                elif choice == 6:
                    add_return(cursor)
                elif choice == 7:
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == 1:
            while True:
                print('1. Information about authors')
                print('2. Information about books')
                print('3. Information about publishers')
                print('4. Information about users')
                print('5. Information about issues')
                print('6. Exit')
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    cursor.execute("SELECT * FROM authors")
                    print('\n')
                    results = cursor.fetchall()
                    for row in results:
                        print(row)
                    print('\n')
                elif choice == 2:
                    cursor.execute("SELECT * FROM books")
                    print('\n')
                    results = cursor.fetchall()
                    for row in results:
                        print(row)
                elif choice == 3:
                    cursor.execute("SELECT * FROM publishers")
                    print('\n')
                    results = cursor.fetchall()
                    for row in results:
                        print(row)
                    print('\n')
                elif choice == 4:
                    cursor.execute("SELECT * FROM users")
                    print('\n')
                    results = cursor.fetchall()
                    for row in results:
                        print(row)
                    print('\n')
                elif choice == 5:
                    cursor.execute("SELECT * FROM issued_books")
                    print('\n')
                    results = cursor.fetchall()
                    for row in results:
                        print(row)
                    print('\n')
                elif choice == 6:
                    break
                else:
                    print("Invalid choice. Please try again.")
                    print('\n')
        elif choice == 3:
            delete_data(cursor)
        elif choice == 4:
            exit(0)

if __name__ == "__main__":
    starting()
    db_connection.close()