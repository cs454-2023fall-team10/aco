import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


class Graph:
    def draw(self):
        pos = graphviz_layout(self.graph, prog="dot")

        nx.draw(self.graph, pos, with_labels=True)
        labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()

    @staticmethod
    def draw_graphs(g1, g2):
        plt.subplot(1, 2, 1)
        pos1 = graphviz_layout(g1.graph, prog="dot")
        nx.draw(g1.graph, with_labels=True, pos=pos1)
        labels = nx.get_edge_attributes(g1.graph, "weight")
        nx.draw_networkx_edge_labels(g1.graph, pos1, edge_labels=labels)
        plt.title("Graph 1")

        plt.subplot(1, 2, 2)
        pos2 = graphviz_layout(g2.graph, prog="dot")
        nx.draw(g2.graph, with_labels=True, pos=pos2)
        labels = nx.get_edge_attributes(g2.graph, "weight")
        nx.draw_networkx_edge_labels(g2.graph, pos1, edge_labels=labels)
        plt.title("Graph 2")

        plt.show()
