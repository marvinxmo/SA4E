import json
import time
import threading
from kafka import KafkaProducer, KafkaConsumer


class FinishSection:

    def __init__(
        self,
        num_laps=3,
    ):
        # Players of form {"id": 1, "position": 0, "laps_completed": 0, "start_time": 0}
        self.num_laps = num_laps
        self.num_finished_players = 0
        self.finished_players = []
        self.name = "finish_section"
        self.successor_name = "start_section"
        self.producer = KafkaProducer(
            bootstrap_servers=["localhost:9095"],
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            api_version=(0, 10),
        )

        self.consumer = KafkaConsumer(
            "finish_section",
            bootstrap_servers=["localhost:9095"],
            value_deserializer=lambda m: json.loads(
                m.decode("utf-8"),
            ),
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
            player["position"] += 1
            player["laps_completed"] += 1
            print(
                f"Player {player['id']} completed {
                  player['laps_completed']}/{self.num_laps} laps"
            )

            if player["laps_completed"] >= self.num_laps:
                player["finish_time"] = time.time()
                player["isFinished"] = True
                self.num_finished_players += 1
                self.finished_players.append(player)
                print(
                    f"Player {player['id']} finished the race in {
                      player['finish_time'] - player['start_time']} seconds"
                )
                continue

            self.producer.send(self.successor_name, player)
            print(
                f"Moved Player {player['id']} from {self.name} to {self.successor_name} (NEXT ROUND)"
            )

    def close_section(self):
        self.consumer.close()
        self.producer.close()
        self.consumer_thread.join()
        print(f"Section {self.name} closed")
