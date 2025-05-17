-- Example SQL Queries

-- 1. Insert a new user
INSERT INTO users (username, email, password_hash)
VALUES ('john_doe', 'john@example.com', 'hashed_password_here');

-- 2. Add a new product
INSERT INTO products (name, description, price, stock_quantity)
VALUES ('Laptop', 'High-performance laptop', 999.99, 10);

-- 3. Create a new order
INSERT INTO orders (user_id, total_amount)
VALUES (1, 1999.98);

-- 4. Add items to an order
INSERT INTO order_items (order_id, product_id, quantity, price_at_time)
VALUES (1, 1, 2, 999.99);

-- 5. Get all products with low stock (less than 5)
SELECT product_id, name, stock_quantity
FROM products
WHERE stock_quantity < 5;

-- 6. Get total sales by user
SELECT u.username, COUNT(o.order_id) as total_orders, SUM(o.total_amount) as total_spent
FROM users u
JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id;

-- 7. Get most popular products
SELECT p.name, SUM(oi.quantity) as total_ordered
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id
ORDER BY total_ordered DESC
LIMIT 5;

-- 8. Update product price
UPDATE products
SET price = 899.99
WHERE product_id = 1;

-- 9. Delete a user (with proper cascade handling)
DELETE FROM users
WHERE user_id = 1;

-- 10. Complex query: Get recent orders with product details
SELECT 
    o.order_id,
    u.username,
    o.order_date,
    o.total_amount,
    GROUP_CONCAT(p.name) as products,
    GROUP_CONCAT(oi.quantity) as quantities
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_date DESC
LIMIT 10; 