import json
import time
import threading
from kafka import KafkaProducer, KafkaConsumer


class StartSection:

    def __init__(self, successor_name):
        # Players of form {"id": 1, "position": 0, "laps_completed": 0, "start_time": 0}
        self.name = "start_section"
        self.successor_name = successor_name
        self.players = []
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.consumer = KafkaConsumer("start_section", bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        
        # Start the consumer thread
        self.consumer_thread = threading.Thread(target=self.forward_players)
        self.consumer_thread.daemon = True
        self.consumer_thread.start()

    def forward_players(self):
        for message in self.consumer:
            player = message.value
            player['position'] = 0
            print(f"Player received at start: {player}")
            self.producer.send(self.successor_name, player)
            print(f"Player sent from start to {self.successor_name}: {player}")

    def add_player(self):
        player = {"id": len(self.players) + 1, "position": 0, "laps_completed": 0, "start_time": 0}
        self.players.append(player)
        return f"New Player created: {player}"
    
    def get_player_count(self):
        return f"Currently {len(self.players)} players registered"
    
    def start_race(self):
        for player in self.players:
            player["start_time"] = time.time()
            self.producer.send(self.successor_name, player)


        