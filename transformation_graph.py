import random
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
        def calc_distance(node1, node2):
            """
            Calculate distance of node embeddings

            실제 유저 시뮬레이션: intent, choice similarity
            Transformation: choice, (intent)

            idea:
                depth 정보 -> 1번 optimize
                    edge가 이미 있을때
                        remove
                    없을때
                        def cal_distance(node1, node2):
                            return distance
                        if cal_distance(node1, node2) < 4
                            ADD_EDGE node1 node2

            1. CG_nodes -> TG_nodes: n^2 ()
            2. TG_nodes -> edges: n^2 (directed complete)


            aciton item
            1. complete에서 directed 없앰
            2. chatbotgraph 만들 때, edge 정보 가져오기
                2-1. remove edge할 때 있을 때만
            3. add edge할 때는 위에 distance
            """
            return random.random()

        """
        complete transformation graph
        n <- nodes of CG
        ->
        m <- nP2 * 2 + n (directed graph is nedded)
        ->
        edges <- m * (m-1) (directed graph is nedded)

        -> n^4
        """
        CG_nodes = CG.graph.nodes.data()
        TG_nodes = []
        for node1 in CG_nodes:
            TG_nodes.append("REMOVE_NODE " + node1[0])
            for node2 in CG_nodes:
                if node1 == node2:
                    continue
                if calc_distance(node1, node2) < 0.5:
                    TG_nodes.append("ADD_EDGE " + node1[0] + " " + node2[0])
                else:
                    TG_nodes.append("REMOVE_EDGE " + node1[0] + " " + node2[0])

        TG = nx.complete_graph(TG_nodes)
        TG.add_weighted_edges_from([(u, v, constants.WEIGHT) for u, v in TG.edges])

        return TG


if __name__ == "__main__":
    CG = ChatbotGraph("general-homepage")
    print(CG)
    TG = TransformationGraph(CG)
    print(TG)
