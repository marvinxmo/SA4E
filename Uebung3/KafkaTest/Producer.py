import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_test_message():
    message = {'id': 15, 'position': 95, 'laps_completed': 0, 'start_time': 9}
    producer.send('finish_section', message)
    producer.flush()
    print(f"Sent message: {message}")

if __name__ == "__main__":
    send_test_message()