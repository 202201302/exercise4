import pymysql.cursors


class LibraryDB:
    def __init__(self):
        self.mydb = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='library',
            charset='utf8'
        )

        self.cursor = self.mydb.cursor()

    def add_book(self, title, author, isbn, status):
        add_book_query = "INSERT INTO Books (Title, Author, ISBN, Status) VALUES (%s, %s, %s, %s)"
        book_data = (title, author, isbn, status)
        self.cursor.execute(add_book_query, book_data)
        self.mydb.commit()

    def find_book_by_id(self, book_id):
        book_query = '''SELECT Books.*, Users.Name, Users.Email, Reservations.ReservationDate
                        FROM Books
                        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                        LEFT JOIN Users ON Reservations.UserID = Users.UserID
                        WHERE Books.BookID = %s'''
        self.cursor.execute(book_query, (book_id,))
        return self.cursor.fetchone()

    def find_reservation_status(self, search_text):
        if search_text[:2] == "LB":
            search_type = "Books.BookID"
            search_value = int(search_text[2:])
        elif search_text[:2] == "LU":
            search_type = "Users.UserID"
            search_value = int(search_text[2:])
        elif search_text[:2] == "LR":
            search_type = "Reservations.ReservationID"
            search_value = int(search_text[2:])
        else:
            search_type = "Books.Title"
            search_value = search_text

        reservation_query = f'''SELECT Books.BookID, Books.Title, Books.Status, Users.UserID, Users.Name, Users.Email, Reservations.ReservationID, Reservations.ReservationDate
                               FROM Books
                               LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                               LEFT JOIN Users ON Reservations.UserID = Users.UserID
                               WHERE {search_type} = %s'''
        self.cursor.execute(reservation_query, (search_value,))
        return self.cursor.fetchone()

    def find_all_books(self):
        all_books_query = '''SELECT Books.*, Users.UserID, Users.Name, Users.Email, Reservations.ReservationID, Reservations.ReservationDate
                             FROM Books
                             LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                             LEFT JOIN Users ON Reservations.UserID = Users.UserID'''
        self.cursor.execute(all_books_query)
        return self.cursor.fetchall()

    def update_book_details(self, book_id, new_title=None, new_author=None, new_isbn=None, new_status=None):
        update_query = "UPDATE Books SET"
        update_data = []

        if new_title:
            update_query += " Title = %s,"
            update_data.append(new_title)
        if new_author:
            update_query += " Author = %s,"
            update_data.append(new_author)
        if new_isbn:
            update_query += " ISBN = %s,"
            update_data.append(new_isbn)
        if new_status:
            update_query += " Status = %s,"
            update_data.append(new_status)

        update_query = update_query.rstrip(",") + " WHERE BookID = %s"
        update_data.append(book_id)

        self.cursor.execute(update_query, update_data)
        self.mydb.commit()

    def delete_book(self, book_id):
        delete_query = "DELETE Books, Reservations FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID WHERE Books.BookID = %s"
        self.cursor.execute(delete_query, (book_id,))
        self.mydb.commit()

    def close(self):
        self.cursor.close()
        self.mydb.close()

def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the book author: ")
    isbn = input("Enter the book ISBN: ")
    status = input("Enter the book status: ")
    library_db.add_book(title, author, isbn, status)
    print("Book added successfully.")

def find_book_by_id():
    book_id = input("Enter the BookID: ")
    book_info = library_db.find_book_by_id(book_id)
    if book_info:
        print("Book found:")
        print("BookID:", book_info[0])
        print("Title:", book_info[1])
        print("Author:", book_info[2])
        print("ISBN:", book_info[3])
        print("Status:", book_info[4])
        print("Reserved By:", book_info[5])
        print("Email:", book_info[6])
        print("Reservation Date:", book_info[7])
    else:
        print("Book not found.")

def find_reservation_status():
    search_text = input("Enter the search text: ")
    reservation_info = library_db.find_reservation_status(search_text)
    if reservation_info:
        print("Reservation found:")
        print("BookID:", reservation_info[0])
        print("Title:", reservation_info[1])
        print("Status:", reservation_info[2])
        print("UserID:", reservation_info[3])
        print("User Name:", reservation_info[4])
        print("Email:", reservation_info[5])
        print("ReservationID:", reservation_info[6])
        print("Reservation Date:", reservation_info[7])
    else:
        print("Reservation not found.")

def find_all_books():
    all_books = library_db.find_all_books()
    if all_books:
        print("All books in the database:")
        for book in all_books:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            print("UserID:", book[5])
            print("User Name:", book[6])
            print("Email:", book[7])
            print("ReservationID:", book[8])
            print("Reservation Date:", book[9])
            print("--------------------")
    else:
        print("No books found in the database.")

def update_book_details():
    book_id = input("Enter the BookID: ")
    new_title = input("Enter the new title (Leave blank to skip): ")
    new_author = input("Enter the new author (Leave blank to skip): ")
    new_isbn = input("Enter the new ISBN (Leave blank to skip): ")
    new_status = input("Enter the new status (Leave blank to skip): ")
    library_db.update_book_details(book_id, new_title, new_author, new_isbn, new_status)
    print("Book details updated successfully.")

def delete_book():
    book_id = input("Enter the BookID: ")
    library_db.delete_book(book_id)
    print("Book deleted successfully.")

# Create an instance of LibraryDB
library_db = LibraryDB()

# Main program loop
while True:
    print("\n--- Library Database Menu ---")
    print("1. Add a new book to the database")
    print("2. Find a book's detail based on BookID")
    print("3. Find a book's reservation status")
    print("4. Find all the books in the database")
    print("5. Modify/update book details based on BookID")
    print("6. Delete a book based on BookID")
    print("7. Exit")
    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_by_id()
    elif choice == "3":
        find_reservation_status()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        update_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        break
    else:
        print("Invalid choice. Please try again.")

# Close the cursor and database connection
library_db.close()