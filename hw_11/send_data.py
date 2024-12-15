from kafka import KafkaProducer
import json

# Создаем продюсера Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Читаем данные из файла и отправляем их в Kafka
with open('data.json') as f:
    data = json.load(f)
    for record in data:
        producer.send('example_topic', value=record)

producer.flush()
producer.close()
