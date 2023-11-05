import matplotlib.pyplot as plt
import networkx as nx
import json
import random

random.seed(42)

DG = nx.DiGraph()
messed_DG = nx.DiGraph()

file_path = "../chatbot-dataset/examples/general-homepage.json"

with open(file_path, 'r') as file:
    data = json.load(file)["sections"]

# for section in data:
#     print(type(section))
#     print(section)
#     print()

for section in data:
    DG.add_node(section['id'])
    DG.nodes[section['id']]['text'] = section['text']

for section in data:
    if section['type'] == 'stop':
        continue
    for button in section['buttons']:
        DG.add_edge(section['id'], button['nextSectionId'])

size = len(DG.nodes)
print(type(DG.nodes))
for node in DG.nodes:
    num_of_indices = random.randrange(size)
    messed_DG.add_node(node)
    messed_DG.nodes[node]['text'] = DG.nodes[node]['text']
    for neighbor in random.sample(list(DG.nodes), num_of_indices):
        messed_DG.add_edge(node, neighbor)
        if not messed_DG.nodes[node]['text']:
            messed_DG.nodes[neighbor]['text'] = DG.nodes[neighbor]['text']

plt.subplot(1, 2, 1)
pos1 = nx.spring_layout(DG)
nx.draw(DG, with_labels=True, pos=pos1)
plt.title("Original chatbot graph")

plt.subplot(1, 2, 2)
pos2 = nx.spring_layout(messed_DG)
nx.draw(messed_DG, with_labels=True, pos=pos2)
plt.title("Intentioanlly messed chatbot graph")

plt.show()