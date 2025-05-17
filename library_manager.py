import sqlite3
from datetime import datetime, timedelta
import sys

class LibraryManager:
    def __init__(self, db_name='library.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish connection to the database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print("Connected to database successfully")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def add_member(self, first_name, last_name, email, phone=None, address=None):
        """Add a new member to the library"""
        try:
            self.cursor.execute('''
                INSERT INTO members (first_name, last_name, email, phone, address, membership_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, phone, address, datetime.now().date()))
            self.conn.commit()
            print(f"Member {first_name} {last_name} added successfully")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding member: {e}")
            return None

    def add_book(self, isbn, title, author, publisher=None, publication_year=None, 
                genre=None, total_copies=1, location=None):
        """Add a new book to the library"""
        try:
            self.cursor.execute('''
                INSERT INTO books (isbn, title, author, publisher, publication_year, 
                                 genre, total_copies, available_copies, location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (isbn, title, author, publisher, publication_year, genre, 
                 total_copies, total_copies, location))
            self.conn.commit()
            print(f"Book '{title}' added successfully")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding book: {e}")
            return None

    def borrow_book(self, book_id, member_id, loan_days=14):
        """Borrow a book from the library"""
        try:
            # Check if book is available
            self.cursor.execute('SELECT available_copies FROM books WHERE book_id = ?', (book_id,))
            available = self.cursor.fetchone()[0]
            
            if available <= 0:
                print("Book is not available for borrowing")
                return False

            # Create loan record
            loan_date = datetime.now().date()
            due_date = loan_date + timedelta(days=loan_days)
            
            self.cursor.execute('''
                INSERT INTO loans (book_id, member_id, loan_date, due_date, status)
                VALUES (?, ?, ?, ?, 'active')
            ''', (book_id, member_id, loan_date, due_date))
            
            # Update available copies
            self.cursor.execute('''
                UPDATE books 
                SET available_copies = available_copies - 1 
                WHERE book_id = ?
            ''', (book_id,))
            
            self.conn.commit()
            print("Book borrowed successfully")
            return True
        except sqlite3.Error as e:
            print(f"Error borrowing book: {e}")
            return False

    def return_book(self, loan_id):
        """Return a borrowed book"""
        try:
            # Get loan details
            self.cursor.execute('''
                SELECT book_id, due_date FROM loans WHERE loan_id = ?
            ''', (loan_id,))
            book_id, due_date = self.cursor.fetchone()
            
            # Update loan record
            self.cursor.execute('''
                UPDATE loans 
                SET return_date = ?, status = 'returned' 
                WHERE loan_id = ?
            ''', (datetime.now().date(), loan_id))
            
            # Update available copies
            self.cursor.execute('''
                UPDATE books 
                SET available_copies = available_copies + 1 
                WHERE book_id = ?
            ''', (book_id,))
            
            # Check for overdue and add fine if necessary
            if datetime.now().date() > due_date:
                days_overdue = (datetime.now().date() - due_date).days
                fine_amount = days_overdue * 0.50  # $0.50 per day
                
                self.cursor.execute('''
                    INSERT INTO fines (loan_id, amount, issue_date, status)
                    VALUES (?, ?, ?, 'unpaid')
                ''', (loan_id, fine_amount, datetime.now().date()))
            
            self.conn.commit()
            print("Book returned successfully")
            return True
        except sqlite3.Error as e:
            print(f"Error returning book: {e}")
            return False

    def search_books(self, title=None, author=None, genre=None):
        """Search for books by various criteria"""
        try:
            query = "SELECT * FROM books WHERE 1=1"
            params = []
            
            if title:
                query += " AND title LIKE ?"
                params.append(f"%{title}%")
            if author:
                query += " AND author LIKE ?"
                params.append(f"%{author}%")
            if genre:
                query += " AND genre = ?"
                params.append(genre)
            
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error searching books: {e}")
            return []

    def get_member_loans(self, member_id):
        """Get all active loans for a member"""
        try:
            self.cursor.execute('''
                SELECT l.loan_id, b.title, l.loan_date, l.due_date
                FROM loans l
                JOIN books b ON l.book_id = b.book_id
                WHERE l.member_id = ? AND l.status = 'active'
            ''', (member_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting member loans: {e}")
            return []

def main():
    # Example usage
    library = LibraryManager()
    library.connect()
    
    try:
        # Add a new member
        member_id = library.add_member(
            "Alice", "Johnson", "alice@example.com",
            "555-1234", "123 Library Lane"
        )
        
        # Add a new book
        book_id = library.add_book(
            "9781234567890", "Python Programming",
            "John Doe", "Tech Books", 2023,
            "Programming", 3, "Tech Section"
        )
        
        # Borrow the book
        if member_id and book_id:
            library.borrow_book(book_id, member_id)
        
        # Search for books
        print("\nSearching for books:")
        books = library.search_books(title="Python")
        for book in books:
            print(f"Found: {book[2]} by {book[3]}")
        
        # Get member's loans
        print("\nMember's active loans:")
        loans = library.get_member_loans(member_id)
        for loan in loans:
            print(f"Loan ID: {loan[0]}, Book: {loan[1]}, Due: {loan[3]}")
            
    finally:
        library.close()

if __name__ == "__main__":
    main() 