import random
import networkx as nx

import constants
from chatbot_graph import ChatbotGraph
from graph import Graph


class TransformationGraph(Graph):
    def __init__(self, CG: ChatbotGraph):
        self.graph = self.create(CG)
        self.pheromones = {}

    def __str__(self):
        return f"TG: {self.graph}"

    def add_pheromone(self, s, e, p):
        if (s, e) not in self.pheromones:
            self.pheromones[(s, e)] = 0
        self.pheromones[(s, e)] += p

    def evaporate(self):
        for (s, e), _ in self.pheromones.items():
            self.pheromones[(s, e)] *= constants.EVAPORATION_RATE

        keys_to_delete = []
        for (s, e), p in self.pheromones.items():
            if p < 1e-4:
                keys_to_delete.append((s, e))

        for key in keys_to_delete:
            del self.pheromones[key]

    def get_pheromone(self, s, e):
        if (s, e) not in self.pheromones:
            return 0
        return self.pheromones[(s, e)]

    def report_pheremone_stats(self):
        print(f"TG num edges with pheromone = {len(self.pheromones)}")

        if len(self.pheromones) > 0:
            # Average pheromone
            print(
                f"TG average pheromone = {sum(self.pheromones.values()) / len(self.pheromones)}"
            )

            # Max pheromone
            print(f"TG max pheromone = {max(self.pheromones.values())}")

    def create(self, CG: ChatbotGraph):
        """
        Transformation Graph Node Rules
        1. REMOVE_NODE
        2. REMOVE_EDGE <v1> <v2> if has edge
        3. ADD_EDGE <v1> <v2> if has shortest path and not far
        """
        # Only consider connected nodes
        CG_nodes = nx.shortest_path(CG.graph, "A").keys()
        TG_nodes = []

        for node1 in CG_nodes:
            # Skip unconnected nodes
            if node1[0] != "A":
                # Start Node can not removed
                TG_nodes.append("REMOVE_NODE " + node1[0])
            for node2 in CG_nodes:
                if node1 == node2:
                    continue

                if CG.graph.has_edge(node1[0], node2[0]):
                    TG_nodes.append("REMOVE_EDGE " + node1[0] + " " + node2[0])
                else:
                    texts = self.get_incoming_texts(CG.graph, node2)
                    if len(texts) > 0:
                        text = random.choice(texts)
                        TG_nodes.append(
                            "ADD_EDGE " + node1[0] + " " + node2[0] + " " + text
                        )

        TG = nx.complete_graph(TG_nodes)
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

    def num_nodes(self):
        return len(self.graph.nodes())

    def num_rm_node(self):
        return len(
            [node for node in self.graph.nodes() if node.startswith("REMOVE_NODE")]
        )

    def num_rm_edge(self):
        return len(
            [node for node in self.graph.nodes() if node.startswith("REMOVE_EDGE")]
        )

    def num_add_edge(self):
        return len([node for node in self.graph.nodes() if node.startswith("ADD_EDGE")])

    def num_edges(self):
        return len(self.graph.edges())

    def print_stats(self):
        print(f"TG: V = {self.num_nodes()}, E = {self.num_edges()}")
        print(f"TG num_rm_node = {self.num_rm_node()}")
        print(f"TG num_rm_edge = {self.num_rm_edge()}")
        print(f"TG num_add_edge = {self.num_add_edge()}")


if __name__ == "__main__":
    CG = ChatbotGraph("lead-homepage")
    print(CG)
    TG = TransformationGraph(CG)
    print(TG)
