import json
import os
import time
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from Sections.StartSection import StartSection
from Sections.NormalSection import NormalSection
from Sections.FinishSection import FinishSection


def load_track_config(track_file):
    my_path = os.path.dirname(__file__)
    try:
        with open(f"{my_path}/CuCuCo/{track_file}", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(
            "Error: TrackConfig.json not found. Please create it using RaceTrack.py first."
        )
        exit(1)


def get_input(prompt, default, cast_func):
    while True:
        user_input = input(prompt)
        if user_input == "":
            return default
        try:
            return cast_func(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid value.")


def initialize_sections(track_config, num_laps):

    sections = {}

    for segment in track_config["segments"]:

        if segment["type"] == "start":
            sections["start_section"] = StartSection(
                successor_name=f"section_{segment['nextSegment']}"
            )

        elif segment["type"] == "normal":

            if segment["nextSegment"] == 1000:
                sections[f"section_{segment['id']}"] = NormalSection(
                    self_name=f"section_{segment['id']}",
                    successor_name="finish_section",
                )
            else:
                sections[f"section_{segment['id']}"] = NormalSection(
                    self_name=f"section_{segment['id']}",
                    successor_name=f"section_{segment['nextSegment']}",
                )

        elif segment["type"] == "finish":
            sections["finish_section"] = FinishSection(num_laps)

    return sections


def shutdown_track(sections):
    for section in sections.values():
        section.producer.close()
        section.consumer.close()
        section.consumer_thread.join()


def main():

    track_config_wish = get_input(
        "Use ExampleTrackConfig.json (1) or MyTrackConfig.json (2): ",
        1,
        lambda x: (
            int(x)
            if int(x) in [1, 2]
            else (_ for _ in ()).throw(ValueError("Only 1 or 2 allowed"))
        ),
    )

    if track_config_wish == 1:
        track_file = "ExampleTrackConfig.json"
    elif track_config_wish == 2:
        track_file = "MyTrackConfig.json"

    track_config = load_track_config(track_file)

    num_players = get_input("Enter number of players (default 1): ", 1, int)
    num_laps = get_input("Enter number of laps (default 3): ", 3, int)

    print("----------------------------------")
    print("Initializing sections...")
    sections = initialize_sections(track_config, num_laps)
    start_section = sections["start_section"]
    finish_section = sections["finish_section"]

    print("----------------------------------")
    print("Adding players...")

    for _ in range(num_players):
        print(start_section.add_player())

    time.sleep(1)

    print("----------------------------------")
    print("Start Race...")
    start_section.start_race()

    while True:
        time.sleep(2)
        if finish_section.num_finished_players == num_players:
            print("Race finished...")
            print("----------------------------------")
            break
        else:
            print("Waiting for all players to finish...")

    print("Race results:")
    for player in finish_section.finished_players:
        print(
            f"Player {player['id']} completed {num_laps} laps in {round(player['finish_time'] - player['start_time'], 4)} seconds"
        )


if __name__ == "__main__":
    main()
