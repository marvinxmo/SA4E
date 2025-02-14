import json
import time
import threading
from kafka import KafkaProducer, KafkaConsumer


class StartSection:

    def __init__(self, successor_name):
        # Players of form {"id": 1, "position": 0, "laps_completed": 0, "start_time": 0, "finish_time": 0}
        self.name = "start_section"
        self.successor_name = successor_name
        self.players = []

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
            "start_section",
            bootstrap_servers=["localhost:9092", "localhost:9093", "localhost:9094"],
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            api_version=(0, 10),
            # group_id="ave_caesar",
        )

        # Start the consumer thread
        self.consumer_thread = threading.Thread(target=self.forward_players)
        self.consumer_thread.daemon = True
        self.consumer_thread.start()

        self.start_event = threading.Event()
        self.player_threads = []

        print(f"{self.name} section initialized")

    def forward_players(self):
        for message in self.consumer:
            player = message.value
            player["position"] = 0
            self.producer.send(self.successor_name, player)
            print(
                f"Moved Player {player['id']} from {self.name} to {self.successor_name}"
            )

    def add_player(self):
        player = {
            "id": len(self.players) + 1,
            "position": 0,
            "laps_completed": 0,
            "start_time": 0,
            "isFinished": False,
            "finish_time": 0,
        }
        self.players.append(player)

        return f"New Player created: {player}"

    def get_player_count(self):
        return f"Currently {len(self.players)} players registered"

    def start_player(self, player):
        # Wait for start event
        self.start_event.wait()
        player["start_time"] = time.time()
        self.producer.send(self.successor_name, player)
        print(f"Player {player['id']} started racing")

    def start_race(self):
        # Create thread for each player
        for player in self.players:
            thread = threading.Thread(target=self.start_player, args=(player,))
            self.player_threads.append(thread)
            thread.start()

        # Trigger start event - all players start simultaneously
        time.sleep(0.5)  # Small delay to ensure all threads are waiting
        print("Ready...")
        time.sleep(0.5)
        print("Set...")
        time.sleep(0.5)
        print("GO!")
        time.sleep(0.5)

        self.start_event.set()
