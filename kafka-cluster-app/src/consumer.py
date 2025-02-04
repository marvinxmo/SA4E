from kafka import KafkaConsumer
from config import KAFKA_BOOTSTRAP_SERVERS, TOPIC_NAME
import json

def create_consumer():
    return KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my_consumer_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        session_timeout_ms=30000,
        heartbeat_interval_ms=10000
    )

def consume_messages():
    consumer = create_consumer()
    print("Starting consumer...")
    try:
        for message in consumer:
            print(f"Received: {message.value}")
    except Exception as e:
        print(f"Error consuming messages: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()