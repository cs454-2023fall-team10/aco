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
        pos1 = graphviz_layout(g1, prog="dot")
        nx.draw(g1, with_labels=True, pos=pos1)
        plt.title("Graph 1")

        plt.subplot(1, 2, 2)
        # pos2 = nx.spring_layout(messed_DG)
        pos2 = graphviz_layout(g2, prog="dot")
        nx.draw(g2, with_labels=True, pos=pos2)
        plt.title("Graph 2")

        plt.show()
