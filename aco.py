import sys
import networkx as nx
import matplotlib.pyplot as plt
import random
import pydot
from networkx.drawing.nx_pydot import graphviz_layout


class Edge:
    def __init__(self, start, end, pheromone, weight):
        self.start = start
        self.end = end
        self.pheromone = pheromone
        self.weight = weight


class Ant:
    def __init__(self, id):
        self.id = id
        self.current_node = 0
        self.route = []
        self.travel_distance = 0

    def __str__(self):
        return f"{self.id}, {self.route}, {self.travel_distance}"

    def reset(self):
        self.current_node = 0
        self.route = []
        self.travel_distance = 0

    def traverse(self, G: nx.Graph):
        while True:
            self.route.append(self.current_node)
            children = list(
                nx.bfs_tree(G, source=self.current_node, depth_limit=1).edges()
            )
            if not children:
                break

            next_edge = self.select(0.5)
            self.current_node = next_edge.end
            self.travel_distance += next_edge.weight

    def select(self, rate):
        edges = list(nx.bfs_tree(G, source=self.current_node, depth_limit=1).edges())
        edges = [
            Edge(
                start=start,
                end=end,
                pheromone=G.get_edge_data(start, end, "pheromone")["pheromone"],
                weight=G.get_edge_data(start, end, "weight")["weight"],
            )
            for start, end in edges
        ]
        edges.sort(key=lambda n: n.pheromone, reverse=True)

        if random.random() < rate:
            next_edge = edges[0]
        else:
            next_edge = random.choice(edges)

        # update_pheromone_locally()

        return next_edge


def make_transformation_graph():
    trans_G = nx.DiGraph()
    trans_G.add_edge(0, 1, weight=2, pheromone=0)
    trans_G.add_edge(0, 2, weight=3, pheromone=0)
    trans_G.add_edge(0, 3, weight=4, pheromone=0)
    trans_G.add_edge(0, 4, weight=5, pheromone=0)

    trans_G.add_edge(1, 5, weight=2, pheromone=0)
    trans_G.add_edge(1, 6, weight=3, pheromone=0)
    trans_G.add_edge(2, 7, weight=4, pheromone=0)
    trans_G.add_edge(2, 8, weight=5, pheromone=0)
    trans_G.add_edge(3, 9, weight=2, pheromone=0)
    trans_G.add_edge(3, 10, weight=3, pheromone=0)
    trans_G.add_edge(4, 11, weight=4, pheromone=0)
    trans_G.add_edge(4, 12, weight=5, pheromone=0)

    return trans_G


def aco(G):
    ants = [Ant(i) for i in range(50)]

    shortest_distance = sys.maxsize
    shortest_path = []

    budget = 1
    count = 0
    while count < budget:
        count += 1
        for ant in ants:
            """
            TODO: traverse in parallel?
            """
            ant.traverse(G)

            if ant.travel_distance < shortest_distance:
                shortest_distance = ant.travel_distance
                shortest_path = ant.route

        # update_pheromone_globally()

        for ant in ants:
            ant.reset()

    for ant in ants:
        print(ant)

    print("shortest: ", shortest_path, shortest_distance)
    return shortest_path


if __name__ == "__main__":
    G = make_transformation_graph()

    shortest_path = aco(G)

    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()
