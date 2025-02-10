CREATE DATABASE crm_db;

-- Create Customers Table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE,
    phone VARCHAR(50),
    address VARCHAR(250)
);

-- Create Products Table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2),
    weight NUMERIC(10, 2)
);

-- Add Data
INSERT INTO customers (name, email, phone, address) VALUES ('Alice Johnson', 'alice@example.com', '555-1234', '123 Maple St, New York, NY'), ('Bob Smith', 'bob@example.com', '555-5678', '456 Oak Ave, Los Angeles, CA'), ('Cathy Lee', 'cathy@example.com', '555-8765', '789 Pine Rd, Chicago, IL');
INSERT INTO products (name, description, price, weight) VALUES ('Laptop', '15-inch screen, 8GB RAM, 256GB SSD', 1200.00, 2.5), ('Smartphone', '128GB storage, 6GB RAM', 800.00, 0.4), ('Headphones', 'Noise-cancelling, wireless', 150.00, 0.3);

-- Create Store Procedures add_customer
CREATE OR REPLACE PROCEDURE add_customer(
    p_name VARCHAR,
    p_email VARCHAR,
    p_phone VARCHAR,
    p_address VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO customers (name, email, phone, address)
    VALUES (p_name, p_email, p_phone, p_address);
END;
$$;