import networkx as nx
import matplotlib.pyplot as plt
from RaceTrack import track


def visualize_track(track_data):
    G = nx.DiGraph()
    segments = track_data["segments"]

    # Knoten und Kanten hinzufügen
    for seg in segments:
        seg_id = seg["id"]
        G.add_node(seg_id, label=seg["type"])
        if seg["nextSegment"] is not None:
            G.add_edge(seg_id, seg["nextSegment"])

    # Standard-Zeichnung
    pos = nx.spring_layout(G, seed=3068)
    nx.draw(G, pos, with_labels=True, node_size=1500, node_color="lightblue")

    # Labels für Knotentypen anzeigen
    # labels = {node: f"{node}\n({data['label']})" for node, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, font_color="black")

    plt.title("Ave Caesar Spielbrett (Netzwerk)")
    plt.show()


if __name__ == "__main__":
    visualize_track(track)
