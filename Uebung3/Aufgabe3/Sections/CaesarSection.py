import json
import time
import threading
from kafka import KafkaProducer, KafkaConsumer
import random


class CaesarSection:
    """
    All Player need to wait a random amount of time (between 1 and 5 seconds)
    to accordingly greet Caesar by kneeling down in front of him.
    In contrast to bottleneck sections, the players are not blocked by eachother.
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

        # Start the consumer thread
        self.consumer_thread = threading.Thread(target=self.forward_players)
        self.consumer_thread.daemon = True
        self.consumer_thread.start()

        print(f"{self.name} section initialized")

    def forward_players(self):
        for message in self.consumer:
            player = message.value
            player["position"] = self.name

            wait_time = random.randint(1, 5)
            print(
                f"Player has to kneel down in front of Caesar for {wait_time} seconds"
            )
            time.sleep(wait_time)

            self.producer.send(self.successor_name, player)
            print(
                f"Moved Player {player['id']} from {self.name} to {self.successor_name}"
            )

    def close_section(self):
        self.consumer.close()
        self.producer.close()
        self.consumer_thread.join()
        print(f"Section {self.name} closed")
