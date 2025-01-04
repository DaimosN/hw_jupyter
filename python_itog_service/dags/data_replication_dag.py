from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
# from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import mysql.connector
from mysql.connector import Error


def transfer_users(mysql_host, mysql_user, mysql_password):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default',
                           host='postgres',
                           user='myuser',
                           password='mypassword')
    # mysql_hook = MySqlHook(mysql_conn_id='mysql_default',
    #                        host=mysql_host,
    #                        user=mysql_user,
    #                        password=mysql_password)

    # Извлечение пользователей из PostgreSQL и вставка в MySQL.
    users = pg_hook.get_records("SELECT user_id, first_name, last_name, email, phone, loyalty_status FROM Users")

    try:
        # Подключение к MySQL
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database='mydatabase'  # Укажите имя вашей базы данных
        )

        if connection.is_connected():
            cursor = connection.cursor()
            for user in users:
                cursor.execute(
                    "INSERT INTO Users (first_name, last_name, email, phone, loyalty_status) VALUES (%s, %s, %s, %s, %s)",
                    user[1:])
            connection.commit()
            cursor.close()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()


def transfer_products_category(mysql_host, mysql_user, mysql_password):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default',
                           host='postgres',
                           user='myuser',
                           password='mypassword')

    product_categories = pg_hook.get_records("SELECT category_id, name, parent_category_id FROM ProductCategories")

    try:
        # Подключение к MySQL
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database='mydatabase'  # Укажите имя вашей базы данных
        )

        if connection.is_connected():
            cursor = connection.cursor()
            for pr_categ in product_categories:
                cursor.execute(
                    "INSERT INTO ProductCategories ( name, parent_category_id ) VALUES (%s, %s)",
                    pr_categ[1:])
            connection.commit()
            cursor.close()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()


def transfer_products(mysql_host, mysql_user, mysql_password):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default',
                           host='postgres',
                           user='myuser',
                           password='mypassword')

    products = pg_hook.get_records(
        'SELECT product_id, "name", description, category_id, price, stock_quantity FROM Products')

    try:
        # Подключение к MySQL
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database='mydatabase'  # Укажите имя вашей базы данных
        )

        if connection.is_connected():
            cursor = connection.cursor()
            for product in products:
                cursor.execute(
                    """INSERT INTO Products ( name, description, category_id, price, stock_quantity ) VALUES (%s, %s, %s, %s, %s)""",
                    product[1:])
            connection.commit()
            cursor.close()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()


def transfer_orders(mysql_host, mysql_user, mysql_password):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default',
                           host='postgres',
                           user='myuser',
                           password='mypassword')

    orders = pg_hook.get_records(
        'SELECT order_id, user_id, order_date, total_amount, status, delivery_date FROM Orders')

    try:
        # Подключение к MySQL
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database='mydatabase'  # Укажите имя вашей базы данных
        )

        if connection.is_connected():
            cursor = connection.cursor()
            for order in orders:
                cursor.execute(
                    """INSERT INTO Orders ( user_id, order_date, total_amount, status, delivery_date ) VALUES (%s, %s, %s, %s, %s)""",
                    order[1:])
            connection.commit()
            cursor.close()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()


def transfer_orders_details(mysql_host, mysql_user, mysql_password):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default',
                           host='postgres',
                           user='myuser',
                           password='mypassword')

    orders_details = pg_hook.get_records(
        'SELECT order_detail_id, order_id, product_id, quantity, price_per_unit, total_price from OrderDetails')

    try:
        # Подключение к MySQL
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database='mydatabase'  # Укажите имя вашей базы данных
        )

        if connection.is_connected():
            cursor = connection.cursor()
            for orders_detail in orders_details:
                cursor.execute(
                    """INSERT INTO OrderDetails ( order_id, product_id, quantity, price_per_unit, total_price ) VALUES (%s, %s, %s, %s, %s)""",
                    orders_detail[1:])
            connection.commit()
            cursor.close()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()


# schedule_interval='0 * * * *'
with DAG('data_replication_dag', start_date=datetime(2025, 1, 1, 16, 0), schedule_interval='@daily') as dag:
    transfer_users_task = PythonOperator(
        task_id='transfer_users',
        python_callable=transfer_users,
        op_kwargs={
            'mysql_host': 'mysql',
            'mysql_user': 'myuser',
            'mysql_password': 'mypassword'
        },
        dag=dag,
    )

    transfer_products_category_task = PythonOperator(
        task_id='transfer_products_category',
        python_callable=transfer_products_category,
        op_kwargs={
            'mysql_host': 'mysql',
            'mysql_user': 'myuser',
            'mysql_password': 'mypassword'
        },
        dag=dag,
    )

    transfer_products_task = PythonOperator(
        task_id='transfer_products',
        python_callable=transfer_products,
        op_kwargs={
            'mysql_host': 'mysql',
            'mysql_user': 'myuser',
            'mysql_password': 'mypassword'
        },
        dag=dag,
    )

    transfer_orders_task = PythonOperator(
        task_id='transfer_orders',
        python_callable=transfer_orders,
        op_kwargs={
            'mysql_host': 'mysql',
            'mysql_user': 'myuser',
            'mysql_password': 'mypassword'
        },
        dag=dag,
    )

    transfer_orders_details_task = PythonOperator(
        task_id='transfer_orders_details',
        python_callable=transfer_orders_details,
        op_kwargs={
            'mysql_host': 'mysql',
            'mysql_user': 'myuser',
            'mysql_password': 'mypassword'
        },
        dag=dag,
    )

transfer_users_task >> transfer_products_category_task >> transfer_products_task >> transfer_orders_task >> transfer_orders_details_task
