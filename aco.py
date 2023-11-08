from collections import namedtuple
import sys
import networkx as nx
import matplotlib.pyplot as plt
import random
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

Edge = namedtuple("Edge", ["start", "end", "data"])


class Ant:
    alpha = 1
    beta = 2
    evaporate_coeff = 0.4
    budget = 5

    def __init__(self, id):
        self.id = id
        self.current_node = random.randrange(10)
        self.route = []
        self.travel_distance = 0

    def __str__(self):
        return f"{self.id}, {self.route}, {self.travel_distance}"

    def reset(self):
        self.current_node = random.randrange(10)
        self.route = []
        self.travel_distance = 0

    def traverse(self, G: nx.DiGraph):
        count = 0
        while count < self.budget:
            count += 1

            next_edge = self.select(G)
            self.route.append(next_edge)
            self.current_node = next_edge.end
            self.travel_distance += next_edge.data["weight"]

    def _calc_probabilities(self, edges):
        """
        p_ij <- tau_ij^alpha * eta^beta / sigma p_ij

        p_ij: probability of select node i to j
        eta: 1 / c_ij
            c_ij: weight of node i to j
        """
        probabilities = []
        for edge in edges:
            # For now, allow to revisit nodes
            # if edge in self.route:
            #     probabilities.append(0)

            pheromone = edge.data["pheromone"]
            importance = 1 / edge.data["weight"]
            probabilities.append(pheromone**self.alpha * importance**self.beta)

        sum_p = sum(probabilities)
        return [p / sum_p for p in probabilities]

    def select(self, G) -> Edge:
        edges = list(G.edges.data(data=True, nbunch=self.current_node))
        edges = [Edge(*e) for e in edges]

        if random.random() < 0.5:
            probabilities = self._calc_probabilities(edges)

            next_edge = random.choices(population=edges, weights=probabilities, k=1)[0]
        else:
            next_edge = random.choice(edges)

        self.update_pheromone_locally(G, next_edge)

        return next_edge

    def update_pheromone_locally(self, G, edge):
        """
        tau_xy <- (1-rho) * tau_xy + rho * tau_0

        tau_xy: pheromone for node x to y
        rho: coefficient of evaporation
        """
        G[edge.start][edge.end]["pheromone"] = (1 - self.evaporate_coeff) * G[
            edge.start
        ][edge.end]["pheromone"]
        G[edge.start][edge.end]["pheromone"] += (
            self.evaporate_coeff * AntColony.initial_pheromone
        )

    def update_pheromone_globally(self, G):
        """
        tau_xy <- (1-rho) * tau_xy + delta tau_xy_k
            delta tau_xy_k = Q / L_k

        tau_xy: pheromone for node x to y
        rho: coefficient of evaporation
        """
        visited = [(edge.start, edge.end) for edge in self.route]
        cost = sum([data["weight"] for _, _, data in self.route])
        for start, end in G.edges():
            G[start][end]["pheromone"] = (1 - self.evaporate_coeff) * G[start][end][
                "pheromone"
            ]
            G[start][end]["pheromone"] += 1 / cost if (start, end) in visited else 0


class AntColony:
    initial_pheromone = 1

    def __init__(self, G: nx.Graph):
        self.G = G

    def init_pheromone(self):
        """
        For testing
        """
        for start, end in self.G.edges():
            if (start, end) in [(1, 3), (3, 4), (4, 5), (5, 7), (7, 9)]:
                # 1 -> 2 -> 4 -> 5 -> 7 -> 9
                self.G[start][end]["weight"] = -1
            else:
                self.G[start][end]["weight"] = 10
            self.G[start][end]["pheromone"] = self.initial_pheromone

    def aco(self):
        self.init_pheromone()

        ants = [Ant(i) for i in range(50)]

        shortest_distance = sys.maxsize
        shortest_path = []
        best_ant = ants[0]

        budget = 50
        count = 0
        while count < budget:
            count += 1
            for ant in ants:
                """
                TODO: traverse in parallel?
                """
                ant.traverse(self.G)

                if ant.travel_distance < shortest_distance:
                    shortest_distance = ant.travel_distance
                    shortest_path = ant.route
                    best_ant = ant

            best_ant.update_pheromone_globally(G)

            for ant in ants:
                ant.reset()

        print("shortest: ")
        for edge in shortest_path:
            print(edge)
        print(shortest_distance)
        return shortest_path


def make_transformation_graph():
    trans_G = nx.complete_graph(10, nx.DiGraph())

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
    # print_graph(G)
