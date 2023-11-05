import matplotlib.pyplot as plt
import networkx as nx
import json

DG = nx.DiGraph()

file_path = "../chatbot-dataset/examples/general-homepage.json"

with open(file_path, 'r') as file:
    data = json.load(file)["sections"]
    print(type(data))
    print(data)

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

nx.draw(DG, with_labels=True)
plt.show()