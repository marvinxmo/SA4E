import json
import time
import threading
from kafka import KafkaProducer, KafkaConsumer


class NormalSection:

    def __init__(self, self_name, successor_name):
        # Players of form {"id": 1, "position": 0, "laps_completed": 0}
        self.name = self_name
        self.successor_name = successor_name
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.consumer = KafkaConsumer(self_name, bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        # Start the consumer thread
        self.consumer_thread = threading.Thread(target=self.forward_players)
        self.consumer_thread.daemon = True
        self.consumer_thread.start()

    def forward_players(self):
        for message in self.consumer:
            player = message.value
            player['position'] += 1

            print(f"Player received at {self.name}: {player}")
            self.producer.send(self.successor_name, player)
            print(f"Player sent from {self.name} to {self.successor_name}: {player}")
