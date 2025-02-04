from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from config import KAFKA_BOOTSTRAP_SERVERS, TOPIC_NAME, REPLICATION_FACTOR
import json
import time


def create_topic():
    try:
        admin = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        topic = NewTopic(
            name=TOPIC_NAME, num_partitions=3, replication_factor=REPLICATION_FACTOR
        )
        admin.create_topics([topic])
        print(f"Topic {TOPIC_NAME} created successfully")
    except Exception as e:
        print(f"Topic creation failed: {e}")


def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all",
    )


def send_messages():
    producer = create_producer()
    for i in range(10):
        message = {"message": f"Message {i}sz"}
        producer.send(TOPIC_NAME, value=message)
        print(f"Sent: {message}")
        time.sleep(1)
    producer.close()


if __name__ == "__main__":
    create_topic()
    send_messages()
