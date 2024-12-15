import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

actions = ["login", "logout", "purchase", "click"]

def generate_action(user_id):
    return {
        "user_id": user_id,
        "action": random.choice(actions),
        "timestamp": (datetime.now() - timedelta(days=random.randint(0, 10))).isoformat()
    }

data = [generate_action(random.randint(1, 10)) for _ in range(100)]

with open('data.json', 'w') as f:
    json.dump(data, f)
