CREATE DATABASE struggle_db;


CREATE TABLE customers (
	customer_id INT PRIMARY KEY,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	email VARCHAR(50),
	phone NUMERIC,
	registration_date DATE,
	loyalty_points NUMERIC
);



CREATE TABLE product (
	product_id INT PRIMARY KEY,
	product_name VARCHAR(50),
	product_description VARCHAR(50),
	brand VARCHAR(50),
	price INT,
	stock_quantity INT
);

CREATE TABLE sales_transaction (
	transaction_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT, 
    transaction_date DATETIME,
    total_spent INT,
	discounts INT,
	employee_name VARCHAR(50),
	payment_method VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);
