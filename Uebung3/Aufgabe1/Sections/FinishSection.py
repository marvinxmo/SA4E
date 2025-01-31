import json
import time
import threading
from kafka import KafkaProducer, KafkaConsumer


class FinishSection:

    def __init__(self, num_laps=3):
        # Players of form {"id": 1, "position": 0, "laps_completed": 0, "start_time": 0}
        self.num_laps = num_laps
        self.name = "finish_section"
        self.successor_name = "start_section"
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.consumer = KafkaConsumer("finish_section", bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

        # Start the consumer thread
        self.consumer_thread = threading.Thread(target=self.forward_players)
        self.consumer_thread.daemon = True
        self.consumer_thread.start()

    def forward_players(self):

        for message in self.consumer:
            player = message.value

            player["position"] += 1
            player["laps_completed"] += 1
            
            if message.value['laps_completed'] == self.num_laps:
                print(f"Player {message.value['id']} finished the race in {time.time() - message.value['start_time']} seconds")
                continue

            print(f"Player received at finish: {player}")
            self.producer.send(self.successor_name, player)
            print(f"Player sent from finish to NEXT_ROUND: {player}")

