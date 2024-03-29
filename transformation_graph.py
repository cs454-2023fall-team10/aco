from os import system
import random
import sys
import networkx as nx
import constants
from chatbot_graph import ChatbotGraph
from graph import Graph


class TransformationGraph(Graph):
    def __init__(self, CG: ChatbotGraph):
        self.graph = self.create(CG)

    def __str__(self):
        return f"TG: {self.graph}"

    def create(self, CG: ChatbotGraph):
        """
        Transformation Graph Node Rules
        1. REMOVE_NODE
        2. REMOVE_EDGE <v1> <v2> if has edge
        3. ADD_EDGE <v1> <v2> if has shortest path and not far
        """
        CG_nodes = CG.graph.nodes.data()
        TG_nodes = []
        for node1 in CG_nodes:
            if node1[0] != "A":
                # Start Node can not removed
                TG_nodes.append("REMOVE_NODE " + node1[0])
            for node2 in CG_nodes:
                if node1 == node2:
                    continue

                if CG.graph.has_edge(node1[0], node2[0]):
                    TG_nodes.append("REMOVE_EDGE " + node1[0] + " " + node2[0])
                elif nx.has_path(CG.graph, node1[0], node2[0]):
                    if (
                        nx.shortest_path_length(CG.graph, node1[0], node2[0])
                        < constants.NODE_DISTANCE_THRESHOLD
                    ):
                        texts = self.get_incoming_texts(CG.graph, node2)
                        text = random.choice(texts)
                        TG_nodes.append(
                            "ADD_EDGE " + node1[0] + " " + node2[0] + " " + text
                        )

        TG = nx.complete_graph(TG_nodes)
        TG.add_weighted_edges_from([(u, v, constants.WEIGHT) for u, v in TG.edges])

        return TG

    @staticmethod
    def get_incoming_texts(graph, node):
        """
        Extract unique incoming edges's text of the node.

        To prevent cycle, exclude some texts.
        """
        exclude = ["이전 단계로", "이전단계"]

        texts = [
            data["text"]
            for _, _, data in graph.in_edges(node[0], data=True)
            if data["text"] not in exclude
        ]

        return list(set(texts))


if __name__ == "__main__":
    CG = ChatbotGraph("lead-homepage")
    print(CG)
    TG = TransformationGraph(CG)
    print(TG)
