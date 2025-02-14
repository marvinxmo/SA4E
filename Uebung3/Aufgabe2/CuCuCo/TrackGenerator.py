import argparse
import json
import random
from typing import Dict, Any, List
import os


def create_race_track(normal_count=5) -> Dict[str, Any]:
    """
    Creates a track dictionary like ExampleRaceTrack.py, but in a random order.

     - Always 1 start_section
     - Always 1 finish_section
     - normal_count (default=5) for Normal sections

    The Tracks can be Visualized using TrackVisualizer.py
    """

    # Start segment
    track_segments: List[Dict[str, Any]] = [
        {"id": "start_section", "type": "start", "nextSegment": None}
    ]

    # 1) Normal segments
    for i in range(normal_count):
        track_segments.append({"id": f"N{i+1}", "type": "normal", "nextSegment": None})

    # Link the pool in a chain
    for i in range(len(track_segments) - 1):
        track_segments[i]["nextSegment"] = track_segments[i + 1]["id"]

    # Create finish segment
    finish_seg = {"id": "finish_section", "type": "finish", "nextSegment": None}

    # Connect the last item to the finish
    last_id = track_segments[-1]["id"]
    track_segments[-1]["nextSegment"] = finish_seg["id"]

    track_segments.append(finish_seg)

    return {"segments": track_segments}


if __name__ == "__main__":

    normal_count = int(input("Enter the number of normal sections (default=5): ") or 5)

    track = create_race_track(normal_count=normal_count)

    mypath = os.path.dirname(__file__)

    # Save the track configuration to a JSON file
    with open(f"{mypath}/MyTrackConfig.json", "w") as f:
        json.dump(track, f, indent=4)

    print("Track configuration saved to MyTrackConfig.json")
