import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

SECTION_COLORS = {
    "start": "green",
    "normal": "lightblue",
    "finish": "gold",
    "bottleneck": "red",
    "split": "orange",
    "caesar": "purple",
}


def add_segment(G: nx.DiGraph, segment):
    seg_id = segment["id"]
    seg_type = segment["type"]
    seg_color = SECTION_COLORS.get(seg_type, "gray")

    if G.has_node(seg_id):
        G.nodes[seg_id]["color"] = seg_color
        G.nodes[seg_id]["section_type"] = seg_type
    else:
        G.add_node(seg_id, color=seg_color, section_type=seg_type)

    if seg_type == "split":
        for path in segment.get("subPaths", []):
            if path:
                # Connect Split to first subpath element
                G.add_edge(seg_id, path[0]["id"])
            for sub_seg in path:
                add_segment(G, sub_seg)
    else:
        next_seg = segment["nextSegment"]
        if next_seg is not None:
            if not G.has_node(next_seg):
                G.add_node(next_seg, color="gray", section_type="unknown")
            G.add_edge(seg_id, next_seg)


def add_segment2(G: nx.DiGraph, segment):
    seg_id = segment["id"]
    seg_type = segment["type"]
    seg_color = SECTION_COLORS.get(seg_type, "gray")

    # Only create node if it doesn't exist yet
    if not G.has_node(seg_id):
        G.add_node(seg_id, color=seg_color, section_type=seg_type)

    if seg_type == "split":
        for path in segment.get("subPaths", []):
            if path:
                first_id = path[0]["id"]
                # Ensure the first node of the path is added before creating edge
                if not G.has_node(first_id):
                    first_color = SECTION_COLORS.get(path[0]["type"], "gray")
                    G.add_node(
                        first_id, color=first_color, section_type=path[0]["type"]
                    )
                G.add_edge(seg_id, first_id)

            # Recursively add all sub-segments
            for sub_seg in path:
                add_segment2(G, sub_seg)
    else:
        next_seg = segment.get("nextSegment")
        if next_seg is not None:
            # Ensure next_seg node is added before edge
            if not G.has_node(next_seg):
                G.add_node(next_seg, color="gray", section_type="unknown")
            G.add_edge(seg_id, next_seg)


def create_track_graph(track_data):
    G = nx.DiGraph()
    for segment in track_data["segments"]:
        add_segment(G, segment)
    return G


def layered_layout(G):
    """
    A BFS-based top-to-bottom layout.
    We try to center each layer horizontally to reduce 'scuffed' visuals.
    """
    # Find start nodes (no incoming edges)
    start_nodes = [n for n, deg in G.in_degree() if deg == 0]
    layer_map = {}
    queue = deque()

    # Initialize BFS
    for s in start_nodes:
        layer_map[s] = 0
        queue.append(s)

    # Standard BFS to assign layers
    while queue:
        current = queue.popleft()
        current_layer = layer_map[current]
        for neighbor in G.successors(current):
            if neighbor not in layer_map:
                layer_map[neighbor] = current_layer + 1
                queue.append(neighbor)

    # Group nodes by layer
    layer_groups = {}
    for node, layer in layer_map.items():
        layer_groups.setdefault(layer, []).append(node)

    # Build positions, layer by layer
    pos = {}
    # Sort layers to ensure 0..N order
    sorted_layers = sorted(layer_groups.keys())
    for layer in sorted_layers:
        nodes = layer_groups[layer]
        count = len(nodes)
        # Spread them out horizontally, centered around x=0
        for i, node in enumerate(nodes):
            x_offset = i - (count - 1) / 2
            pos[node] = (x_offset * 3, -layer * 3)  # tweak spacing as desired
    return pos


def draw_track_graph(G, title="Track Visualization"):
    pos = layered_layout(G)
    color_map = [data.get("color", "gray") for _, data in G.nodes(data=True)]
    # pos = nx.circular_layout(G)
    nx.draw(
        G,
        pos,
        # with_labels=True,
        arrows=True,
        node_color=color_map,
        node_size=1500,
        edge_color="black",
        font_color="black",
    )

    labels = {
        n: f"{data["section_type"]}"  # ({data.get('section_type', 'unknown')})"
        for n, data in G.nodes(data=True)
    }
    nx.draw_networkx_labels(G, pos, labels)
    plt.title(title)
    plt.show()


import os
import json

if __name__ == "__main__":
    # Load the track config from RaceTrack.py’s JSON (assuming it’s in the same folder)
    current_dir = os.path.dirname(__file__)
    track_json_path = os.path.join(current_dir, "ExampleTrackConfig.json")
    with open(track_json_path, "r", encoding="utf-8") as f:
        track_data = json.load(f)

    G = create_track_graph(track_data)
    draw_track_graph(G, title="Ave Caesar Track")
