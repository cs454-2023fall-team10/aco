from collections import namedtuple
import time
import networkx as nx
import random

import constants
from chatbot_graph import ChatbotGraph
from graph import Graph
from transformation_graph import TransformationGraph

Edge = namedtuple("Edge", ["start", "end", "data"])


DEBUG = True


def debug(*args):
    if DEBUG:
        print("[DEBUG]", *args)


class Ant:
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
        probabilities = [1.0 + edge.data["pheromone"] for edge in edges]
        sum_p = sum(probabilities)
        return [p / sum_p for p in probabilities]

    def select(self, G) -> Edge:
        edges = list(G.edges.data(data=True, nbunch=self.current_node))
        edges = [
            Edge(*e) for e in edges if e[1] != "START"
        ]  # Exclude edge when end is "START".

        if random.random() < constants.RANDOM_CHOICE_RATE:
            # Random choice
            next_edge = random.choice(edges)
            return next_edge
        else:
            probabilities = self._calc_probabilities(edges)
            next_edge = random.choices(population=edges, weights=probabilities, k=1)[0]
            return next_edge

    def update_pheromone(self, G, fitness):
        """
        tau_xy <- (1-rho) * tau_xy + delta tau_xy_k
            delta tau_xy_k = Q / L_k

        tau_xy: pheromone for node x to y
        rho: coefficient of evaporation
        """
        visited = [(edge.start, edge.end) for edge in self.route]

        for start, end in visited:
            G[start][end]["pheromone"] += fitness

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

        # TG statistics
        self.TG.print_stats()

    def init_pheromone(self):
        for node in list(self.TG.graph.nodes()):
            self.TG.graph.add_edge("START", node, weight=constants.WEIGHT)

        for start, end in self.TG.graph.edges():
            self.TG.graph[start][end]["pheromone"] = self.initial_pheromone

    def aco(self):
        self.init_pheromone()

        ants = [Ant(i) for i in range(constants.ANT_COUNT)]

        best_fitness = self.CG.fitness
        shortest_path = []

        count = 0
        while count < self.budget:
            count += 1
            start = time.time()

            fitnesses = []

            for ant in ants:
                ant.traverse(self.TG.graph)

                new_CG = self.CG.copy()
                transformation_path = ant.convert_route_to_transformation_path()

                try:
                    new_CG.transform(transformation_path)
                except:
                    # transformation_path is not valid, do not count this ant.
                    continue

                new_CG.evaluate()
                fitnesses.append(new_CG.fitness)

                if new_CG.fitness > best_fitness:
                    # Best fitness per whole ACO.
                    best_fitness = new_CG.fitness
                    shortest_path = transformation_path

            # Update pheromone
            # normalize fitness values among ants
            min_fitness = min(fitnesses)
            max_fitness = max(fitnesses)
            fitnesses = [
                (f - min_fitness) / (max_fitness - min_fitness) for f in fitnesses
            ]
            for ant, fitness in zip(ants, fitnesses):
                ant.update_pheromone(self.TG.graph, fitness)

            for ant in ants:
                ant.reset()

            # Evaporate
            for s, e in self.TG.graph.edges():
                self.TG.graph[s][e]["pheromone"] *= 1 - constants.EVAPORATION_RATE

            print(
                f"Iteration {count}: best_fitness = {best_fitness}, best_fitness_in_epoch: {max_fitness}, elasped time: {time.time() - start:.4f}s"
            )

            if count % 5 == 0:
                print(f"Shortest path in iteration {count}: {shortest_path}")

        print(f"Shortest path: {shortest_path}")
        print(best_fitness)
        return shortest_path


if __name__ == "__main__":
    CG = ChatbotGraph("kakaotalk-faq-231129-small-mingled-003")
    ant_colony = AntColony(CG)

    # Starting fitness
    CG.evaluate()
    print(f"Initial fitness: {CG.fitness}")

    # Show original graph
    # CG.draw()

    # Run ACO
    shortest_path = ant_colony.aco()
    optimized_CG = CG.copy()
    optimized_CG.transform(shortest_path)

    # Show optimized graph
    Graph.draw_graphs(CG, optimized_CG)

# if __name__ == "__main__":
# Graph.draw(ChatbotGraph("kakaotalk-faq-231129-small"))
# Graph.draw(ChatbotGraph("kakaotalk-faq-231129-small-mingled-001"))
# Graph.draw(ChatbotGraph("kakaotalk-faq-231129-small-mingled-002"))
# Graph.draw(ChatbotGraph("kakaotalk-faq-231129-small-mingled-003"))
