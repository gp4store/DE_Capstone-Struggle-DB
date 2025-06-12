


CREATE DATABASE struggle_db;

CREATE TABLE customers (
	customer_id INT AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	email VARCHAR(100),
	phone VARCHAR(50),			
	registration_date DATE,
	loyalty_points NUMERIC
);

CREATE TABLE product (
	product_id INT AUTO_INCREMENT PRIMARY KEY,
	product_name VARCHAR(50),
	product_description VARCHAR(200),
	brand VARCHAR(50),
	size_item VARCHAR(50),
	price DECIMAL(10,2),
	stock_quantity INT
);

CREATE TABLE sales_transaction (
    customer_id INT,
    product_id INT, 
	quantity INT,
    total_amount DECIMAL(10,2),
	order_status VARCHAR(15),
	order_date TIMESTAMP,
	shipping_address VARCHAR(200),
	employee_name VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);