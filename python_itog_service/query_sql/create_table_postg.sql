-- Таблица Users
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    loyalty_status VARCHAR(10) CHECK (loyalty_status IN ('Gold', 'Silver', 'Bronze'))
);

-- Таблица Products
CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    category_id INT,
    price DECIMAL(10, 2),
    stock_quantity INT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица Orders
CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20) CHECK (status IN ('Pending', 'Completed')),
    delivery_date TIMESTAMP
);

-- Таблица OrderDetails
CREATE TABLE OrderDetails (
    order_detail_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES Orders(order_id),
    product_id INT REFERENCES Products(product_id),
    quantity INT,
    price_per_unit DECIMAL(10, 2),
    total_price DECIMAL(10, 2)
);

-- Таблица ProductCategories
CREATE TABLE ProductCategories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    parent_category_id INT REFERENCES ProductCategories(category_id)
);

--====================================================================================

-- Заполнение таблицы Users
INSERT INTO Users (first_name, last_name, email, phone, loyalty_status)
VALUES 
('Иван', 'Иванов', 'ivan@example.com', '+79001234567', 'Gold'),
('Петр', 'Петров', 'petr@example.com', '+79007654321', 'Silver');

-- Заполнение таблицы ProductCategories
INSERT INTO ProductCategories (name)
VALUES 
('Электроника'),
('Одежда');

-- Заполнение таблицы Products
INSERT INTO Products (name, description, category_id, price, stock_quantity)
VALUES 
('Смартфон', 'Современный смартфон с большим экраном', 1, 50000.00, 100),
('Футболка', 'Удобная футболка из хлопка', 2, 1500.00, 200);

-- Заполнение таблицы Orders и OrderDetails
INSERT INTO Orders (user_id, total_amount, status)
VALUES 
(1, 51500.00, 'Completed');

INSERT INTO OrderDetails (order_id, product_id, quantity, price_per_unit, total_price)
VALUES 
(1, 1, 1, 50000.00, 50000.00),
(1, 2, 10, 1500.00, 15000.00);
