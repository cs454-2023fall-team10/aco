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
    alpha = 0.5
    evaporate_coeff = 0.4

    def __init__(self, id):
        self.id = id
        self.current_node = 0
        self.route = []
        self.travel_distance = 0
        self.visited = set()

    def __str__(self):
        return f"{self.id}, {self.route}, {self.travel_distance}"

    def reset(self):
        self.current_node = 0
        self.route = []
        self.travel_distance = 0
        self.visited = set()  # 대신 Budget을 두는게 맞지 않을까?

    def traverse(self, G: nx.DiGraph):
        while True:
            if self.current_node in self.visited:
                break

            self.route.append(self.current_node)
            self.visited.add(self.current_node)
            children = list(
                nx.bfs_tree(G, source=self.current_node, depth_limit=1).edges()
            )
            if not children:
                break

            next_edge = self.select()
            self.current_node = next_edge.end
            self.travel_distance += next_edge.weight

    def select(self):
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

        if random.random() < self.alpha:
            next_edge = edges[0]
        else:
            next_edge = random.choice(edges)

        self.update_pheromone_locally()

        return next_edge

    def update_pheromone_locally(self):
        pass

    def update_pheromone_globally(self):
        pass


class AntColony:
    def __init__(self, G):
        self.G = G

    def init_pheromone(self):
        for start, end in self.G.edges():
            self.G[start][end]["weight"] = random.randrange(0, 10)
            self.G[start][end]["pheromone"] = 0

    def aco(self):
        self.init_pheromone()

        ants = [Ant(i) for i in range(50)]

        shortest_distance = sys.maxsize
        shortest_path = []
        best_ant = ants[0]

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
                    best_ant = ant

            best_ant.update_pheromone_globally()

            for ant in ants:
                ant.reset()

        print("shortest: ", shortest_path, shortest_distance)
        return shortest_path


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

    trans_G.add_edge(5, 13, weight=2, pheromone=0)
    trans_G.add_edge(6, 14, weight=3, pheromone=0)
    trans_G.add_edge(7, 15, weight=4, pheromone=0)
    trans_G.add_edge(8, 16, weight=5, pheromone=0)
    trans_G.add_edge(9, 17, weight=2, pheromone=0)
    trans_G.add_edge(10, 18, weight=3, pheromone=0)
    trans_G.add_edge(11, 19, weight=4, pheromone=0)
    trans_G.add_edge(12, 20, weight=5, pheromone=0)

    trans_G.add_edge(5, 21, weight=2, pheromone=0)
    trans_G.add_edge(6, 22, weight=3, pheromone=0)
    trans_G.add_edge(7, 23, weight=4, pheromone=0)
    trans_G.add_edge(8, 24, weight=5, pheromone=0)
    trans_G.add_edge(9, 25, weight=2, pheromone=0)
    trans_G.add_edge(10, 26, weight=3, pheromone=0)
    trans_G.add_edge(11, 27, weight=4, pheromone=0)
    trans_G.add_edge(12, 28, weight=5, pheromone=0)
    # trans_G = nx.random_geometric_graph(20, radius=0.4, seed=3)

    return trans_G


def print_graph(G):
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


if __name__ == "__main__":
    G = make_transformation_graph()
    ant_colony = AntColony(G)
    shortest_path = ant_colony.aco()
    print_graph(G)
