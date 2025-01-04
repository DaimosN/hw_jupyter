# from pyspark.sql import SparkSession
#
# # Создание Spark сессии
# spark = SparkSession.builder \
#     .appName("Kafka Consumer") \
#     .getOrCreate()
#
# # Чтение данных из Kafka Topics Users и Products
# users_df = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "kafka:9092") \
#     .option("subscribe", "users") \
#     .option("startingOffsets", "earliest")\
#     .load()
#
# products_df = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "kafka:9092") \
#     .option("subscribe", "products") \
#     .option("startingOffsets", "earliest")\
#     .load()
#
# # Преобразование данных из формата JSON в DataFrame
# users_parsed_df = users_df.selectExpr("CAST(value AS STRING) as json")
# products_parsed_df = products_df.selectExpr("CAST(value AS STRING) as json")
#
#
# def write_to_postgres(df, table_name):
#     try:
#         print(f"Writing to {table_name}: {df.count()} records")
#         df.write \
#             .format("jdbc") \
#             .option("url", "jdbc:postgresql://postgres:5432/mydatabase") \
#             .option("dbtable", table_name) \
#             .option("user", "myuser") \
#             .option("password", "mypassword") \
#             .mode("append") \
#             .save()
#     except Exception as e:
#         print(f"Error writing to PostgreSQL: {e}")
#
#
# # Используем foreachBatch для записи данных в PostgreSQL
# users_parsed_df.writeStream \
#     .foreachBatch(lambda df, epochId: write_to_postgres(df, "Users")) \
#     .outputMode("append") \
#     .start()
#
# products_parsed_df.writeStream \
#     .foreachBatch(lambda df, epochId: write_to_postgres(df, "Products")) \
#     .outputMode("append") \
#     .start()
#
# spark.streams.awaitAnyTermination()
from confluent_kafka import Consumer, KafkaError
import psycopg2
import json

# Конфигурация PostgreSQL
db_config = {
    'dbname': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'postgres',
    'port': 5432
}


# Функция для записи данных в PostgreSQL
def write_to_postgres(data, table_name):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Пример вставки данных в таблицу
        if table_name == "Users":
            insert_query = "INSERT INTO Users (first_name, last_name, email, phone, loyalty_status) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (
            data['first_name'], data['last_name'], data['email'], data['phone'], data['loyalty_status']))
        elif table_name == "Products":
            insert_query = "INSERT INTO Products (name, description, category_id, price, stock_quantity) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (
            data['name'], data['description'], data['category_id'], data['price'], data['stock_quantity']))

        conn.commit()
        print(f"Inserted into {table_name}: {data}")

    except Exception as e:
        print(f"Error writing to PostgreSQL: {e}")
    finally:
        cursor.close()
        conn.close()


# Конфигурация потребителя Kafka
conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['users', 'products'])

# Чтение сообщений из Kafka и запись в PostgreSQL
try:
    while True:
        msg = consumer.poll(1.0)  # Ожидание сообщения в течение 1 секунды
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                break

        # Десериализация сообщения
        message_value = json.loads(msg.value().decode('utf-8'))

        # Определение таблицы на основе топика
        if msg.topic() == 'users':
            write_to_postgres(message_value, "Users")
        elif msg.topic() == 'products':
            write_to_postgres(message_value, "Products")

finally:
    consumer.close()
