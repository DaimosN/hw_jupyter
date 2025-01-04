from airflow import DAG
# from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import mysql.connector
from mysql.connector import Error


def create_user_activity_view(mysql_host, mysql_user, mysql_password):
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
            cursor.execute(
                """
               CREATE OR REPLACE VIEW user_activity AS 
               SELECT 
                   u.user_id,
                   u.first_name,
                   u.last_name,
                   COUNT(o.order_id) AS total_orders,
                   SUM(o.total_amount) AS total_spent,
                   u.loyalty_status 
               FROM Users u 
               LEFT JOIN Orders o ON u.user_id = o.user_id 
               GROUP BY u.user_id;
                """)
            connection.commit()
            cursor.close()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()


def create_product_sales_view(mysql_host, mysql_user, mysql_password):
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
            cursor.execute(
                """
               CREATE OR REPLACE VIEW product_sales AS 
               SELECT 
                   p.product_id,
                   p.name AS product_name,
                   SUM(od.quantity) AS total_sold_quantity,
                   SUM(od.total_price) AS total_revenue 
               FROM Products p 
               JOIN OrderDetails od ON p.product_id = od.product_id 
               GROUP BY p.product_id;
                """)
            connection.commit()
            cursor.close()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            connection.close()


with DAG('analytics_views_dag', start_date=datetime(2024, 12, 29), schedule_interval='@daily') as dag:
    create_user_activity_view_task = PythonOperator(
        task_id='create_user_activity_view',
        python_callable=create_user_activity_view,
        op_kwargs={
            'mysql_host': 'mysql',
            'mysql_user': 'myuser',
            'mysql_password': 'mypassword'
        },
        dag=dag,
    )

    create_product_sales_view_task = PythonOperator(
        task_id='create_product_sales_view',
        python_callable=create_product_sales_view,
        op_kwargs={
            'mysql_host': 'mysql',
            'mysql_user': 'myuser',
            'mysql_password': 'mypassword'
        },
        dag=dag,
    )

create_user_activity_view_task >> create_product_sales_view_task
