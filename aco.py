from collections import namedtuple
import sys
import time
import networkx as nx
import random

import constants
from chatbot_graph import ChatbotGraph
from graph import Graph
from transformation_graph import TransformationGraph

Edge = namedtuple("Edge", ["start", "end", "data"])


class Ant:
    alpha = constants.ALPHA
    beta = constants.BETA
    evaporation_rate = constants.EVAPORATION_RATE
    budget = constants.LENGTH_OF_PATH

    def __init__(self, id):
        self.id = id
        self.current_node = "START"
        self.route = []
        self.travel_distance = 0

    def __str__(self):
        return f"{self.id}, {self.route}, {self.travel_distance}"

    def reset(self):
        self.current_node = "START"
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
            pheromone = edge.data["pheromone"]
            importance = 1 / edge.data["weight"]
            probabilities.append(pheromone**self.alpha * importance**self.beta)

        sum_p = sum(probabilities)
        return [p / sum_p for p in probabilities]

    def select(self, G) -> Edge:
        edges = list(G.edges.data(data=True, nbunch=self.current_node))
        edges = [
            Edge(*e) for e in edges if e[1] != "START"
        ]  # Exclude edge when end is "START".

        if random.random() < constants.RANDOM_CHOICE_RATE:
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
        G[edge.start][edge.end]["pheromone"] = (1 - self.evaporation_rate) * G[
            edge.start
        ][edge.end]["pheromone"]
        G[edge.start][edge.end]["pheromone"] += (
            self.evaporation_rate * AntColony.initial_pheromone
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
            G[start][end]["pheromone"] = (1 - self.evaporation_rate) * G[start][end][
                "pheromone"
            ]
            G[start][end]["pheromone"] += 1 / cost if (start, end) in visited else 0

        print(f"ant: {self.id}")
        for edge in self.route:
            print(edge)
        print(cost)

    def convert_route_to_transformation_path(self):
        """
        EX)
        route:
        [Edge(start='START', end='REMOVE_NODE I', data={'weight': 1, 'pheromone': 0.5464705452296552}),
         Edge(start='REMOVE_NODE I', end='REMOVE_EDGE H J', data={'weight': 1, 'pheromone': 0.39553318404096}),
         Edge(start='REMOVE_EDGE H J', end='REMOVE_NODE C', data={'weight': 1, 'pheromone': 0.3867572576256})]

        ->
        transformation_path:
        ["REMOVE_NODE I", "REMOVE_EDGE H J", "REMOVE_NODE C]
        """
        transformation_path = []
        for path in self.route:
            transformation_path.append(path.end)

        return transformation_path


class AntColony:
    initial_pheromone = constants.INITIAL_PHEROMONE
    budget = constants.ITERATION_BUDGET

    def __init__(self, CG: ChatbotGraph):
        self.CG = CG
        self.CG.evaluate()
        self.TG = TransformationGraph(CG)

    def init_pheromone(self):
        for node in list(self.TG.graph.nodes()):
            self.TG.graph.add_edge("START", node, weight=constants.WEIGHT)

        for start, end in self.TG.graph.edges():
            self.TG.graph[start][end]["pheromone"] = self.initial_pheromone

    def aco(self):
        self.init_pheromone()

        ants = [Ant(i) for i in range(constants.ANT_COUNT)]

        fitness = self.CG.fitness
        shortest_path = []

        count = 0
        while count < self.budget:
            count += 1
            start = time.time()
            best_ant = ants[0]
            best_ant_fitness = self.CG.fitness
            for ant in ants:
                ant.traverse(self.TG.graph)

                new_CG = self.CG.copy()
                transformation_path = ant.convert_route_to_transformation_path()
                new_CG.transform(transformation_path)
                new_CG.evaluate()

                if new_CG.fitness > best_ant_fitness:
                    # Best ant per iteration can update pheromone.
                    best_ant = ant
                    best_ant_fitness = new_CG.fitness

                if new_CG.fitness > fitness:
                    # Best fitness per whole ACO.
                    fitness = new_CG.fitness
                    shortest_path = transformation_path

            best_ant.update_pheromone_globally(self.TG.graph)
            print("fitness:", fitness)

            for ant in ants:
                ant.reset()

            print(f"{count}: elasped time: {time.time() - start:.4f}s")

        print("shortest: ")
        for edge in shortest_path:
            print(edge)

        return shortest_path, fitness


if __name__ == "__main__":
    CG = ChatbotGraph("lead-homepage")
    ant_colony = AntColony(CG)

    shortest_path = ant_colony.aco()
    optimized_CG = CG.copy()
    optimized_CG.transform(shortest_path)

    Graph.draw_graphs(CG, optimized_CG)


def run_another(file_name) :
    CG = ChatbotGraph(file_name)
    ant_colony = AntColony(CG)

    shortest_path, fitness = ant_colony.aco()
    optimized_CG = CG.copy()
    optimized_CG.transform(shortest_path)

    return fitness, optimized_CG

def draw_back(file_name, optimized_CG) :
    CG = ChatbotGraph(file_name)
    Graph.draw_graphs(CG, optimized_CG)
