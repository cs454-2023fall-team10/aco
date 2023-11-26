import networkx as nx
import json

from graph import Graph


class ChatbotGraph(Graph):
    def __init__(self, file_path):
        self.file_path = file_path
        self.graph: nx.DiGraph = self.create(file_path)
        self.fitness = 0

    def __str__(self):
        return f"CG: {self.graph}"

    def create(self, path):
        file_path = f"chatbot-dataset/examples/{path}.json"
        with open(file_path, "r") as file:
            data = json.load(file)["sections"]

        CG = nx.DiGraph()

        for section in data:
            CG.add_node(section["id"])
            CG.nodes[section["id"]]["text"] = f"\"{section['text']}\""

        for section in data:
            if section["type"] == "stop":
                continue
            for button in section["buttons"]:
                CG.add_edge(section["id"], button["nextSectionId"], text=button["text"])

        return CG

    def transform(self, transformation_paths):
        """
        Transform ChatbotGraph to the path found using ACO
        """

        def execute(path):
            operator, operands = path.split(maxsplit=1)

            match operator:
                case "REMOVE_NODE":
                    self.graph.remove_node(operands)
                case "REMOVE_EDGE":
                    l, r = operands.split()
                    self.graph.remove_edge(l, r)
                case "ADD_EDGE":
                    l, r = operands.split()
                    self.graph.add_edge(l, r)
                case _:
                    pass

        try:
            for path in transformation_paths:
                execute(path)
        except:
            """
            If a transfrom execution is failed,
            penalize chatbotGraph by converting empty graph
            """
            self.graph = nx.DiGraph()

    def evaluate(self):
        from fitness import fitness

        self.fitness = fitness.fitness(self.graph, self.file_path)

    def copy(self):
        copied = ChatbotGraph(self.file_path)
        copied.graph = self.graph.copy()
        return copied


if __name__ == "__main__":
    CG = ChatbotGraph("lead-homepage")
    CG.evaluate()
    CG_copy = CG.copy()

    CG.draw()
    print(CG)
    CG.transform(["REMOVE_NODE A"])
    CG.draw()
    print(CG)
    CG.transform(["REMOVE_EDGE I K"])
    CG.draw()
    print(CG)

    print(CG_copy)
