import sqlite3
from datetime import datetime

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect('ecommerce.db')
    return conn

def create_tables(conn):
    """Create the database tables."""
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()

def add_user(conn, username, email, password_hash):
    """Add a new user to the database."""
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (username, email, password_hash)
    VALUES (?, ?, ?)
    ''', (username, email, password_hash))
    conn.commit()
    return cursor.lastrowid

def add_product(conn, name, description, price, stock_quantity):
    """Add a new product to the database."""
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO products (name, description, price, stock_quantity)
    VALUES (?, ?, ?, ?)
    ''', (name, description, price, stock_quantity))
    conn.commit()
    return cursor.lastrowid

def get_products(conn):
    """Get all products from the database."""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    return cursor.fetchall()

def main():
    # Create a database connection
    conn = create_connection()
    
    try:
        # Create tables
        create_tables(conn)
        
        # Add some sample data
        user_id = add_user(conn, 'test_user', 'test@example.com', 'hashed_password')
        print(f"Added user with ID: {user_id}")
        
        product_id = add_product(conn, 'Test Product', 'A test product', 99.99, 10)
        print(f"Added product with ID: {product_id}")
        
        # Get and display all products
        products = get_products(conn)
        print("\nAll products in database:")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[3]}")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    main() 