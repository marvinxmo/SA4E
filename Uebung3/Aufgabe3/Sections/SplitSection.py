import json
import time
import threading
import random
from kafka import KafkaProducer, KafkaConsumer
from Sections.StartSection import StartSection
from Sections.NormalSection import NormalSection
from Sections.FinishSection import FinishSection
from Sections.BottleneckSection import BottleneckSection
from Sections.CaesarSection import CaesarSection


class SplitSection:

    def __init__(self, self_name, sub_paths):
        # Players of form {"id": 1, "position": 0, "laps_completed": 0}
        self.name = self_name
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

        # Create all sections from subPaths
        self.subSections = []

        for path in sub_paths:

            for section in path:
                # Can contain all section types except start
                if section["type"] == "normal":
                    self.subSections.append(
                        NormalSection(section["id"], section["nextSegment"])
                    )
                elif section["type"] == "finish":
                    self.subSections.append(FinishSection())
                elif section["type"] == "bottleneck":
                    self.subSections.append(
                        BottleneckSection(section["id"], section["nextSegment"])
                    )
                elif section["type"] == "caesar":
                    self.subSections.append(
                        CaesarSection(section["id"], section["nextSegment"])
                    )

                elif section["type"] == "split":
                    self.subSections.append(
                        SplitSection(section["id"], section["subPaths"])
                    )
                else:
                    raise ValueError(f"Unknown section type {section['type']}")

    def forward_players(self):
        for message in self.consumer:

            player = message.value
            player["position"] = self.name

            # Choose a random subpath the player will take
            choose_subPath = random.choice(range(len(self.subSections)))
            send_to_section = self.subSections[choose_subPath]

            print(
                f"Player {player['id']} chose SubPath {choose_subPath} at Split {self.name}"
            )

            self.producer.send(send_to_section.name, player)
            print(
                f"Moved Player {player['id']} from {self.name} to {send_to_section.name}"
            )

    def close_section(self):

        for section in self.subSections:
            section.close_section()

        self.consumer.close()
        self.producer.close()
        self.consumer_thread.join()
        print(f"Section {self.name} closed")
