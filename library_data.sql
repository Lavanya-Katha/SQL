-- Sample Data Insertion

-- Insert sample members
INSERT INTO members (first_name, last_name, email, phone, address, membership_date, membership_status)
VALUES 
    ('John', 'Smith', 'john.smith@email.com', '555-0101', '123 Main St', '2023-01-15', 'active'),
    ('Emily', 'Johnson', 'emily.j@email.com', '555-0102', '456 Oak Ave', '2023-02-20', 'active'),
    ('Michael', 'Brown', 'm.brown@email.com', '555-0103', '789 Pine Rd', '2023-03-10', 'active');

-- Insert sample authors
INSERT INTO authors (first_name, last_name, birth_date, nationality)
VALUES 
    ('George', 'Orwell', '1903-06-25', 'British'),
    ('Jane', 'Austen', '1775-12-16', 'British'),
    ('J.K.', 'Rowling', '1965-07-31', 'British');

-- Insert sample books
INSERT INTO books (isbn, title, author, publisher, publication_year, genre, total_copies, available_copies, location)
VALUES 
    ('9780451524935', '1984', 'George Orwell', 'Signet Classic', 1949, 'Dystopian', 5, 3, 'Fiction A1'),
    ('9780141439518', 'Pride and Prejudice', 'Jane Austen', 'Penguin Classics', 1813, 'Romance', 3, 2, 'Fiction B2'),
    ('9780747532743', 'Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 'Bloomsbury', 1997, 'Fantasy', 4, 1, 'Fiction C3');

-- Insert book-author relationships
INSERT INTO book_authors (book_id, author_id)
VALUES 
    (1, 1),
    (2, 2),
    (3, 3);

-- Insert sample loans
INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date, status)
VALUES 
    (1, 1, '2023-04-01', '2023-04-15', NULL, 'active'),
    (2, 2, '2023-04-05', '2023-04-19', '2023-04-18', 'returned'),
    (3, 3, '2023-04-10', '2023-04-24', NULL, 'active');

-- Useful Queries

-- 1. Find all books currently on loan
SELECT b.title, m.first_name, m.last_name, l.loan_date, l.due_date
FROM books b
JOIN loans l ON b.book_id = l.book_id
JOIN members m ON l.member_id = m.member_id
WHERE l.status = 'active';

-- 2. Find overdue books
SELECT b.title, m.first_name, m.last_name, l.loan_date, l.due_date
FROM books b
JOIN loans l ON b.book_id = l.book_id
JOIN members m ON l.member_id = m.member_id
WHERE l.status = 'active' AND l.due_date < CURDATE();

-- 3. Find most popular books
SELECT b.title, COUNT(l.loan_id) as loan_count
FROM books b
LEFT JOIN loans l ON b.book_id = l.book_id
GROUP BY b.book_id
ORDER BY loan_count DESC
LIMIT 5;

-- 4. Find members with overdue books
SELECT m.first_name, m.last_name, m.email, m.phone,
       COUNT(l.loan_id) as overdue_count
FROM members m
JOIN loans l ON m.member_id = l.member_id
WHERE l.status = 'active' AND l.due_date < CURDATE()
GROUP BY m.member_id;

-- 5. Find available books by genre
SELECT title, author, available_copies
FROM books
WHERE available_copies > 0
ORDER BY genre, title;

-- 6. Calculate total fines for a member
SELECT m.first_name, m.last_name, SUM(f.amount) as total_fines
FROM members m
JOIN loans l ON m.member_id = l.member_id
JOIN fines f ON l.loan_id = f.loan_id
WHERE f.status = 'unpaid'
GROUP BY m.member_id;

-- 7. Find books by author
SELECT b.title, b.publication_year, b.genre
FROM books b
JOIN book_authors ba ON b.book_id = ba.book_id
JOIN authors a ON ba.author_id = a.author_id
WHERE a.first_name = 'George' AND a.last_name = 'Orwell';

-- 8. Get member borrowing history
SELECT m.first_name, m.last_name, b.title, l.loan_date, l.return_date
FROM members m
JOIN loans l ON m.member_id = l.member_id
JOIN books b ON l.book_id = b.book_id
WHERE m.member_id = 1
ORDER BY l.loan_date DESC; 