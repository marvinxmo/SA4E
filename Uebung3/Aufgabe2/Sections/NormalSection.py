import json
import time
import threading
from kafka import KafkaProducer, KafkaConsumer


class NormalSection:

    def __init__(self, self_name, successor_name):
        # Players of form {"id": 1, "position": 0, "laps_completed": 0}
        self.name = self_name
        self.successor_name = successor_name
        self.producer = KafkaProducer(
            bootstrap_servers=["localhost:9092", "localhost:9093", "localhost:9094"],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            api_version=(0, 10),
            acks="all",
            retries=2,
            retry_backoff_ms=500,
            metadata_max_age_ms=5000,
            max_in_flight_requests_per_connection=1,
        )

        self.consumer = KafkaConsumer(
            self_name,
            bootstrap_servers=["localhost:9092", "localhost:9093", "localhost:9094"],
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            api_version=(0, 10),
            # group_id="ave_caesar",
        )

        # Start the consumer thread
        self.consumer_thread = threading.Thread(target=self.forward_players)
        self.consumer_thread.daemon = True
        self.consumer_thread.start()

        print(f"{self.name} section initialized")

    def forward_players(self):
        for message in self.consumer:
            player = message.value
            player["position"] += 1

            self.producer.send(self.successor_name, player)
            print(
                f"Moved Player {player['id']} from {self.name} to {self.successor_name}"
            )
