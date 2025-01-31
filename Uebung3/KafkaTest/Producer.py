import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_test_message():
    message = {"test": "This is a test message21114"}
    producer.send('test-topic', message)
    producer.flush()
    print(f"Sent message: {message}")

if __name__ == "__main__":
    send_test_message()