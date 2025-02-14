import json
import time
import threading
from kafka import KafkaProducer, KafkaConsumer
import random


class BottleneckSection:
    """
    This section is a bottleneck, meaning that only one player can pass through at a time.
    Each Player blocks the bottleneck for a random amount of time (between 1 and 3 seconds).
    """

    def __init__(self, self_name, successor_name):

        # Players of form {"id": 1, "position": 0, "laps_completed": 0}
        self.name = self_name
        self.successor_name = successor_name
        self.producer = KafkaProducer(
            bootstrap_servers=["localhost:9095"],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            api_version=(0, 10),
        )

        self.consumer = KafkaConsumer(
            self_name,
            bootstrap_servers=["localhost:9095"],
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            api_version=(0, 10),
        )

        # Bottleneck feature
        self.blocked = False

        # Start the consumer thread
        self.consumer_thread = threading.Thread(target=self.forward_players)
        self.consumer_thread.daemon = True
        self.consumer_thread.start()

        print(f"{self.name} section initialized")

    def forward_players(self):
        for message in self.consumer:
            player = message.value

            if self.blocked:
                print(f"Player {player['id']} is blocked by the bottleneck")
                while self.blocked:
                    time.sleep(0.2)

            self.blocked = True
            player["position"] = self.name
            wait_time = random.randint(1, 3)
            print(
                f"Player {player['id']} is blocking bottleneck {self.name} for {wait_time} seconds"
            )
            time.sleep(wait_time)
            self.blocked = False

            self.producer.send(self.successor_name, player)
            print(
                f"Moved Player {player['id']} from {self.name} to {self.successor_name}"
            )

    def close_section(self):
        self.consumer.close()
        self.producer.close()
        self.consumer_thread.join()
        print(f"Section {self.name} closed")
