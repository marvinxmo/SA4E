import json
from kafka import KafkaConsumer

consumer = KafkaConsumer('finish_section', bootstrap_servers='localhost:9092', auto_offset_reset='earliest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

def consume_test_message():
    for message in consumer:
        #print(f"Received message: {message.value}")
        #break  # Exit after receiving the first message
        print(f"{message.value}")

if __name__ == "__main__":
    consume_test_message()