import networkx as nx
import json

from graph import Graph


class ChatbotGraph(Graph):
    def __init__(self, file_path):
        self.graph: nx.DiGraph = self.create(file_path)

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
                CG.add_edge(section["id"], button["nextSectionId"])

        return CG

    def messup(self):
        messed_CG = nx.DiGraph()
        # Mess up the original graph randomly.
        # size = len(DG.nodes)
        # for node in DG.nodes:
        #     num_of_indices = random.randrange(size)
        #     messed_DG.add_node(node)
        #     messed_DG.nodes[node]['text'] = f"\"{DG.nodes[node]['text']}\""
        #     for neighbor in random.sample(list(DG.nodes), num_of_indices):
        #         messed_DG.add_edge(node, neighbor)
        #         if not messed_DG.nodes[node]['text']:
        #             messed_DG.nodes[neighbor]['text'] = f"\"{DG.nodes[neighbor]['text']}\""

        # Hard-coded messed chatbot graph to make transforamtion graph conveniently.
        messed_CG = self.graph.copy()
        removed_edges = [
            ("Q", "R"),
            ("Q", "V"),
            ("R", "S"),
            ("R", "T"),
            ("R", "U"),
            ("O", "P"),
            ("O", "A"),
            ("S", "V"),
            ("S", "R"),
            ("T", "V"),
            ("T", "R"),
            ("U", "V"),
            ("U", "R"),
        ]
        added_edges = [
            ("Q", "J"),
            ("Q", "K"),
            ("J", "S"),
            ("J", "T"),
            ("K", "U"),
            ("I", "R"),
            ("I", "V"),
            ("M", "O"),
            ("N", "P"),
        ]
        messed_CG.remove_edges_from(removed_edges)
        messed_CG.add_edges_from(added_edges)

        self.graph = messed_CG

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

    def evaluate():
        """
        Evaluate ChatbotGraph
        """
        pass


if __name__ == "__main__":
    CG = ChatbotGraph("general-homepage")
    # CG2 = ChatbotGraph("general-homepage")
    # CG2.messup()
    # Graph.draw_graphs(CG.graph, CG2.graph)
    CG.draw()
    print(CG)
    CG.transform(["REMOVE_NODE A"])
    CG.draw()
    print(CG)
    CG.transform(["REMOVE_EDGE I K"])
    CG.draw()
    print(CG)
