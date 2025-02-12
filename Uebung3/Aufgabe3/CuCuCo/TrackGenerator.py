import argparse
import json
import random
from typing import Dict, Any, List
import os


def create_race_track(
    bottleneck_count=1, split_count=1, caesar_count=1, normal_count=5
) -> Dict[str, Any]:
    """
    Creates a track dictionary like ExampleRaceTrack.py, but in a random order.

     - Always 1 start_section
     - Always 1 finish_section
     - bottleneck_count (default=1) for Bottleneck sections
     - split_count (default=1), each with subPaths (2 subpaths, each 3 normal sections), for Split sections
     - caesar_count (default=1) for Caesar sections
     - normal_count (default=5) for Normal sections

    Split segments will have 2 subpaths, each with 3 normal sections.
    You can change the generated json File (MyTrackConfig.json) to make more complex tracks.
    See ExampleTrackConfig.json for an example.

    The Tracks can be Visualized using TrackVisualizer.py
    """

    # Start segment
    track_segments: List[Dict[str, Any]] = [
        {"id": "start_section", "type": "start", "nextSegment": None}
    ]

    # Generate a pool of "randomizable" segments
    random_pool: List[Dict[str, Any]] = []

    # 1) Normal segments
    for i in range(normal_count):
        random_pool.append({"id": f"N{i+1}", "type": "normal", "nextSegment": None})

    # 2) Bottleneck segments
    for i in range(bottleneck_count):
        random_pool.append({"id": f"B{i+1}", "type": "bottleneck", "nextSegment": None})

    # 3) Caesar segments
    for i in range(caesar_count):
        random_pool.append({"id": f"C{i+1}", "type": "caesar", "nextSegment": None})

    # 4) Split segments
    # Each split has subPaths with 2 subpaths, each path has 3 normal sections
    # We'll keep these out of the random pool, so they're placed after the random chain
    for i in range(split_count):
        # Actual split segment id
        base_id = f"S{i+1}"
        split_seg = {"id": base_id, "type": "split", "subPaths": []}
        # subPaths
        num_subpaths = 2
        for sp_idx in range(1, num_subpaths + 1):
            path_list: List[Dict[str, Any]] = []

            # Each subpath has 3 normal sections
            for seg_idx in range(1, 4):
                path_list.append(
                    {
                        "id": f"{base_id}.{sp_idx}.{seg_idx}",
                        "type": "normal",
                        "nextSegment": f"{base_id}.{sp_idx}.{seg_idx+1}",
                    }
                )
            split_seg["subPaths"].append(path_list)
        random_pool.append(split_seg)

    # Shuffle the random pool
    random.shuffle(random_pool)

    # Link the pool in a chain
    for i in range(len(random_pool) - 1):
        random_pool[i]["nextSegment"] = random_pool[i + 1]["id"]

    # Attach the first in the pool to start
    if random_pool:
        track_segments[0]["nextSegment"] = random_pool[0]["id"]

    # Add the random_pool to main list
    track_segments.extend(random_pool)

    # Create finish segment
    finish_seg = {"id": "finish_section", "type": "finish", "nextSegment": None}

    # Connect the last item to the finish
    last_id = track_segments[-1]["id"]
    track_segments[-1]["nextSegment"] = finish_seg["id"]

    track_segments.append(finish_seg)

    for segment in track_segments:
        if segment["type"] == "split":
            nextSegmentAfterTheSplit = segment["nextSegment"]
            for path in segment["subPaths"]:
                path[-1]["nextSegment"] = nextSegmentAfterTheSplit

    return {"segments": track_segments}


if __name__ == "__main__":

    bottleneck_count = int(input("Enter the number of bottlenecks (default=1): ") or 1)
    split_count = int(input("Enter the number of splits (default=1): ") or 1)
    caesar_count = int(input("Enter the number of caesar sections (default=1): ") or 1)
    normal_count = int(input("Enter the number of normal sections (default=5): ") or 5)

    track = create_race_track(
        bottleneck_count=bottleneck_count,
        split_count=split_count,
        caesar_count=caesar_count,
        normal_count=normal_count,
    )

    mypath = os.path.dirname(__file__)

    # Save the track configuration to a JSON file
    with open(f"{mypath}/MyTrackConfig.json", "w") as f:
        json.dump(track, f, indent=4)

    print("Track configuration saved to MyTrackConfig.json")
