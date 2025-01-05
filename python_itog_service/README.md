1) Запуск сервисов
   - docker compose up airflow-init -d
   - docker compose up postgres mysql airflow-webserver airflow-scheduler zookeeper kafka spark spark-master spark-worker -d
2) Выполнить скрипты sql для создания таблиц из директории query_sql. Выполнить внутри docker контейнеров или через графическую оболочку (Dbeaver)
3) Команды для consumer и producer (выполнить внутри spark контейнера)
   - spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 /path/to/your/producer.py
   - python consumer.py
