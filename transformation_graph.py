import networkx as nx
import matplotlib.pyplot as plt
import json


def make_transformation_graph():
    file_path = "chatbot-dataset/examples/general-homepage.json"
    with open(file_path, "r") as file:
        data = json.load(file)["sections"]

    ids = [section["id"] for section in data]
    nodes = []
    for id in ids:
        nodes.append("REMOVE_NODE " + id)
    for id1 in ids:
        for id2 in ids:
            if id1 == id2:
                continue
            nodes.append("REMOVE_EDGE " + id1 + " " + id2)
            nodes.append("ADD_EDGE " + id1 + " " + id2)

    TG = nx.complete_graph(nodes, nx.DiGraph())
    TG.add_weighted_edges_from([(u, v, 1) for u, v in TG.edges])

    valid_nodes = [
        "REMOVE_EDGE Q J",
        "REMOVE_EDGE Q K",
        "REMOVE_EDGE J S",
        "REMOVE_EDGE J T",
        "REMOVE_EDGE K U",
        "REMOVE_EDGE I R",
        "REMOVE_EDGE I V",
        "REMOVE_EDGE M O",
        "REMOVE_EDGE N P",
        "ADD_EDGE Q R",
        "ADD_EDGE Q V",
        "ADD_EDGE R S",
        "ADD_EDGE R T",
        "ADD_EDGE R U",
        "ADD_EDGE O P",
        "ADD_EDGE O A",
        "ADD_EDGE S V",
        "ADD_EDGE S R",
        "ADD_EDGE T V",
        "ADD_EDGE T R",
        "ADD_EDGE U V",
        "ADD_EDGE U R",
    ]

    for node1 in valid_nodes:
        for node2 in valid_nodes:
            if node1 == node2:
                continue
            TG[node1][node2]["weight"] = -1

    return TG
