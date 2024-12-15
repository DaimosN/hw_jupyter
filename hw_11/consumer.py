from kafka import KafkaConsumer
from collections import Counter
import json

# Создаем консьюмера Kafka
consumer = KafkaConsumer(
    'example_topic',
    bootstrap_servers='localhost:29092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

action_counter = Counter()

for message in consumer:
    action = message.value['action']
    action_counter[action] += 1

# Выводим пользователей с наибольшим количеством действий (click, purchase)
print("Количество действий по типам:", dict(action_counter))
