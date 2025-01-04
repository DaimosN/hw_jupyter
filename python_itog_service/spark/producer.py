from pyspark.sql import SparkSession
from pyspark.sql import Row
import json
import random

# Создание Spark сессии
spark = SparkSession.builder \
    .appName("Kafka Producer") \
    .getOrCreate()

# Генерация данных для пользователей
users = []
for i in range(10):
    user = {
        # 'user_id': i,
        'first_name': f'User{i}',
        'last_name': f'Last{i}',
        'email': f'user{i}@example.com',
        'phone': f'+7900123456{i}',
        # 'registration_date': '2024-01-01',
        'loyalty_status': random.choice(['Gold', 'Silver', 'Bronze'])
    }
    users.append(Row(**user))

# Генерация данных для продуктов
products = []
for i in range(10):
    product = {
        # 'product_id': i,
        'name': f'Product{i}',
        'description': f'Description for Product{i}',
        'category_id': random.randint(1, 5),
        'price': round(random.uniform(10.0, 100.0), 2),
        'stock_quantity': random.randint(1, 100),
        # 'creation_date': '2024-01-01'
    }
    products.append(Row(**product))

# Создание DataFrame для пользователей и продуктов
users_df = spark.createDataFrame(users)
products_df = spark.createDataFrame(products)

# Конфигурация Kafka
kafka_bootstrap_servers = "kafka:9092"
users_topic = "users"
products_topic = "products"

# Отправка данных пользователей в Kafka
users_df.selectExpr("to_json(struct(*)) AS value") \
    .write \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("topic", users_topic) \
    .save()

# Отправка данных продуктов в Kafka
products_df.selectExpr("to_json(struct(*)) AS value") \
    .write \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("topic", products_topic) \
    .save()

spark.stop()
