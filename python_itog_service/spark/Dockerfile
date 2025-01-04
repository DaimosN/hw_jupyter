FROM bitnami/spark:3.5.4

# Копируем скрипт запуска и файлы producer/consumer
COPY producer.py /opt/spark/producer.py
COPY consumer.py /opt/spark/consumer.py

RUN pip install confluent-kafka psycopg2-binary
COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf
# Устанавливаем рабочую директорию
WORKDIR /opt/spark
