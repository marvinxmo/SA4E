import json
import os


# Sections
# normal - normal forward to the next section
# caesar - pause for a random amount of time to greet casear
# split - player can choose between (at least) two paths
# bottleneck - only one player at a time can be in this field. He pause for a random amount of time.


# Define the track segments and their connections
track = {
    "segments": [
        # Start always has id 0 and type "start"
        {"id": "0", "type": "start", "nextSegment": "1"},
        {
            "id": "1",
            "type": "split",
            "subPaths": [
                [
                    {"id": "1.1.1", "type": "normal", "nextSegment": "1.1.2"},
                    {"id": "1.1.2", "type": "normal", "nextSegment": "1.1.3"},
                    {"id": "1.1.3", "type": "normal", "nextSegment": "2"},
                ],
                [
                    {"id": "1.2.1", "type": "normal", "nextSegment": "1.2.2"},
                    {"id": "1.2.2", "type": "normal", "nextSegment": "1.2.3"},
                    {"id": "1.2.3", "type": "normal", "nextSegment": "2"},
                ],
            ],
        },
        {"id": 2, "type": "normal", "nextSegment": 3},
        {"id": 3, "type": "normal", "nextSegment": 4},
        {"id": 4, "type": "normal", "nextSegment": 5},
        {"id": 5, "type": "normal", "nextSegment": 6},
        {"id": 6, "type": "normal", "nextSegment": 7},
        {"id": 7, "type": "normal", "nextSegment": 8},
        {"id": 8, "type": "normal", "nextSegment": 9},
        {"id": 9, "type": "normal", "nextSegment": 1000},
        # Finish always has id 1000 and type "finish"
        {"id": 1000, "type": "finish", "nextSegment": None},
    ]
}


mypath = os.path.dirname(__file__)

# Save the track configuration to a JSON file
with open(f"{mypath}/TrackConfig.json", "w") as f:
    json.dump(track, f, indent=4)

print("Track configuration saved to track_config.json")
