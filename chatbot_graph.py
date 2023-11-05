import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import json
import random


random.seed(42)

file_path = "../chatbot-dataset/examples/general-homepage.json"
with open(file_path, 'r') as file:
    data = json.load(file)["sections"]

# for section in data:
#     print(type(section))
#     print(section)
#     print()

def make_chatbot_graphs(data):
    DG = nx.DiGraph()
    messed_DG = nx.DiGraph()

    for section in data:
        DG.add_node(section['id'])
        DG.nodes[section['id']]['text'] = f"\"{section['text']}\""

    for section in data:
        if section['type'] == 'stop':
            continue
        for button in section['buttons']:
            DG.add_edge(section['id'], button['nextSectionId'])

    # Mess up the original graph randomly.
    # size = len(DG.nodes)
    # for node in DG.nodes:
    #     num_of_indices = random.randrange(size)
    #     messed_DG.add_node(node)
    #     messed_DG.nodes[node]['text'] = f"\"{DG.nodes[node]['text']}\""
    #     for neighbor in random.sample(list(DG.nodes), num_of_indices):
    #         messed_DG.add_edge(node, neighbor)
    #         if not messed_DG.nodes[node]['text']:
    #             messed_DG.nodes[neighbor]['text'] = f"\"{DG.nodes[neighbor]['text']}\""

    # Hard-coded messed chatbot graph to make transforamtion graph conveniently.
    messed_DG = DG.copy()
    removed_edges = [('Q', 'R'), ('Q', 'V'), ('R', 'S'), ('R', 'T'), ('R', 'U'), ('O', 'P'), ('O', 'A'), ('S', 'V'), ('S', 'R'), ('T', 'V'), ('T', 'R'), ('U', 'V'), ('U', 'R')]
    added_edges = [('Q', 'J'), ('Q', 'K'), ('J', 'S'), ('J', 'T'), ('K', 'U'), ('I', 'R'), ('I', 'V'), ('M', 'O'), ('N', 'P')]
    messed_DG.remove_edges_from(removed_edges)
    messed_DG.add_edges_from(added_edges)

    plt.subplot(1, 2, 1)
    pos1 = graphviz_layout(DG, prog="dot")
    nx.draw(DG, with_labels=True, pos=pos1)
    plt.title("Original chatbot graph")

    plt.subplot(1, 2, 2)
    # pos2 = nx.spring_layout(messed_DG)
    pos2 = graphviz_layout(messed_DG, prog="dot")
    nx.draw(messed_DG, with_labels=True, pos=pos2)
    plt.title("Intentioanlly messed chatbot graph")

    plt.show()

make_chatbot_graphs(data)