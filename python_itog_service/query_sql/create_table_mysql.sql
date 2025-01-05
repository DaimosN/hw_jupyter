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

CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    user_id BIGINT UNSIGNED,  -- Изменено на BIGINT UNSIGNED
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20) CHECK (status IN ('Pending', 'Completed')),
    delivery_date TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)  -- Убедитесь, что внешний ключ указывает на правильный столбец
);

-- Таблица OrderDetails
CREATE TABLE OrderDetails (
    order_detail_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED,  -- Используем BIGINT UNSIGNED
    product_id BIGINT UNSIGNED,  -- Используем BIGINT UNSIGNED
    quantity INT,
    price_per_unit DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),  -- Внешний ключ на Orders
    FOREIGN KEY (product_id) REFERENCES Products(product_id)  -- Внешний ключ на Products
);

-- Таблица ProductCategories
CREATE TABLE ProductCategories (
    category_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    parent_category_id BIGINT UNSIGNED,  -- Используем BIGINT UNSIGNED для связи с родительской категорией
    FOREIGN KEY (parent_category_id) REFERENCES ProductCategories(category_id)  -- Внешний ключ на саму себя
);
