import json
import os

# Define the track segments and their connections
track = {
    "segments": [

        # Start always has id 0 and type "start"
        {"id": 0, "type": "start", "nextSegment": 1},


        {"id": 1, "type": "normal", "nextSegment": 2},
        {"id": 2, "type": "normal", "nextSegment": 3},
        {"id": 3, "type": "normal", "nextSegment": 4},
        {"id": 4, "type": "normal", "nextSegment": 5},
        {"id": 5, "type": "normal", "nextSegment": 6},
        {"id": 6, "type": "normal", "nextSegment": 7},
        {"id": 7, "type": "normal", "nextSegment": 8},
        {"id": 8, "type": "normal", "nextSegment": 9},
        {"id": 9, "type": "normal", "nextSegment": 1000},


        # Finish always has id 1000 and type "finish"
        {"id": 1000, "type": "finish", "nextSegment": None}
    ]
}


mypath = os.path.dirname(__file__)

# Save the track configuration to a JSON file
with open(f"{mypath}/TrackConfig.json", 'w') as f:
    json.dump(track, f, indent=4)

print("Track configuration saved to track_config.json")