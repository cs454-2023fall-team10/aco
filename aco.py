from collections import namedtuple
import time
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

    def __str__(self):
        return f"{self.id}, {self.route}"

    def reset(self):
        self.current_node = "START"
        self.route = []

    def traverse(self, TG):
        count = 0
        while count < self.budget:
            count += 1

            next_edge = self.select(TG)
            self.route.append(next_edge)
            self.current_node = next_edge[1]

    def _calc_probabilities(self, TG, edges):
        probabilities = [1e-3 + TG.get_pheromone(e[0], e[1]) for e in edges]
        sum_p = sum(probabilities)
        return [p / sum_p for p in probabilities]

    def select(self, TG) -> Edge:
        edges = list(TG.graph.edges.data(nbunch=self.current_node))
        if random.random() < constants.RANDOM_CHOICE_RATE:
            next_edge = random.choice(edges)
            return next_edge
        else:
            probabilities = self._calc_probabilities(TG, edges)
            next_edge = random.choices(population=edges, weights=probabilities, k=1)[0]
            return next_edge

    def update_pheromone(self, TG, amount):
        visited = [(edge[0], edge[1]) for edge in self.route]

        for start, end in visited:
            TG.add_pheromone(start, end, amount)

    def convert_route_to_transformation_path(self):
        transformation_path = []
        for path in self.route:
            transformation_path.append(path[1])

        return transformation_path


class AntColony:
    iterations = constants.ITERATION_BUDGET

    def __init__(self, CG: ChatbotGraph):
        self.CG = CG
        self.CG.evaluate()
        self.TG = TransformationGraph(CG)
        self.TG.print_stats()

    def init_pheromone(self):
        for node in list(self.TG.graph.nodes()):
            self.TG.graph.add_edge("START", node)

    def aco(self):
        self.init_pheromone()

        ants = [Ant(i) for i in range(constants.ANT_COUNT)]

        best_fitness = self.CG.fitness
        shortest_path = []

        count = 0
        while count < self.iterations:
            count += 1
            start = time.time()

            ant_and_fitnesses = []

            for ant in ants:
                ant.traverse(self.TG)

                new_CG = self.CG.copy()
                transformation_path = ant.convert_route_to_transformation_path()

                try:
                    new_CG.transform(transformation_path)
                    new_CG.evaluate()
                    this_fitness = new_CG.fitness
                    ant_and_fitnesses.append((ant, this_fitness))
                except:
                    this_fitness = 0
                    ant_and_fitnesses.append((ant, this_fitness))

                if this_fitness > best_fitness:
                    best_fitness = this_fitness
                    shortest_path = transformation_path

            top_ants = sorted(ant_and_fitnesses, key=lambda x: x[1], reverse=True)
            for ant, fitness in top_ants[: len(top_ants) // 10]:
                ant.update_pheromone(self.TG, fitness)

            for ant in ants:
                ant.reset()

            self.TG.evaporate()

            print(
                f"Iteration {count}: best_fitness = {best_fitness}, elasped time: {time.time() - start:.4f}s"
            )

            print(
                f"Min fitness: {top_ants[-1][1]}, Max fitness: {top_ants[0][1]}, Avg fitness: {sum([x[1] for x in top_ants]) / len(top_ants):.4f}"
            )

            self.TG.report_pheremone_stats()

            if count % 5 == 0:
                print(f"Shortest path in iteration {count}: {shortest_path}")

        print(f"Shortest path: {shortest_path}")
        print(best_fitness)
        return shortest_path


if __name__ == "__main__":
    CG = ChatbotGraph("kakaotalk-faq-231204-mini-mingled")
    CG.evaluate()
    print(CG.fitness)
    # ant_colony = AntColony(CG)

    # # Starting fitness
    # CG.evaluate()
    # print(f"Initial fitness: {CG.fitness}")

    # CG_original = ChatbotGraph("kakaotalk-faq-231204-mini")
    # CG_original.evaluate()
    # print(f"Original fitness: {CG_original.fitness}")

    # # Show original graph
    # # CG.draw()

    # # Run ACO
    # shortest_path = ant_colony.aco()
    # optimized_CG = CG.copy()
    # optimized_CG.transform(shortest_path)

    # # Show optimized graph
    # Graph.draw_graphs(CG, optimized_CG)

# if __name__ == "__main__":
# Graph.draw(ChatbotGraph("kakaotalk-faq-231129-small"))
# Graph.draw(ChatbotGraph("kakaotalk-faq-231129-small-mingled-001"))
# Graph.draw(ChatbotGraph("kakaotalk-faq-231129-small-mingled-002"))
# Graph.draw(ChatbotGraph("kakaotalk-faq-231129-small-mingled-003"))
