import random
import networkx as nx
import matplotlib.pyplot as plt


class Graph:

    def __init__(self, numVertex, numEdges, colors) -> None:
        # To create a connected graph, the number of edges must be greater than the number of vertices minus 1
        if numEdges < numVertex - 1:
            raise Exception(
                "The number of edges must be greater than the number of vertices minus 1")

        self.numVertex = numVertex
        self.numEdges = numEdges
        self.vertex = [i for i in range(numVertex)]
        self.edges = []
        self.nxGraph = nx.Graph()
        if type(colors) != list:
            raise Exception("Colors must be a list")
        self.colors = colors

    def buildEdges(self):
        isConnex = False

        while (not isConnex):
            connections = []
            for i in range(self.numEdges):
                # choose two random nodes
                node1 = random.choice(self.vertex)
                node2 = random.choice(self.vertex)
                while (node1 == node2):
                    node2 = random.choice(self.vertex)

                # tuple to represent the edge
                aresta = (node1, node2)
                aresta = tuple(sorted(aresta))

                # to avoid duplicate edges
                while (aresta in connections):
                    node1 = random.choice(self.vertex)
                    node2 = random.choice(self.vertex)
                    while (node1 == node2):
                        node2 = random.choice(self.vertex)
                    aresta = (node1, node2)
                    aresta = tuple(sorted(aresta))

                connections.append(aresta)

            isConnex = self.connexGraph(connections)

        # [(1, 4), (0, 4), (2, 3), (0, 3), (1, 2), (0, 1)]
        self.connections = connections

        # {1: [4, 2, 0], 4: [1, 0], 0: [4, 3, 1], 2: [3, 1], 3: [2, 0]}
        self.vertexConnected = {}
        for i in self.connections:
            node1, node2 = i
            if node1 and node2 not in self.vertexConnected:
                self.vertexConnected[node1] = [node2]
                self.vertexConnected[node2] = [node1]
            elif node1 not in self.vertexConnected and node2 in self.vertexConnected:
                self.vertexConnected[node1] = [node2]
                self.vertexConnected[node2].append(node1)
            elif node1 in self.vertexConnected and node2 not in self.vertexConnected:
                self.vertexConnected[node2] = [node1]
                self.vertexConnected[node1].append(node2)
            else:
                self.vertexConnected[node1].append(node2)
                self.vertexConnected[node2].append(node1)

        print(self.connections)
        print(self.vertexConnected)

    def drawGraph(self):
        for node1, node2 in self.connections:
            self.nxGraph.add_edge(node1, node2)

        nx.draw(self.nxGraph)
        plt.show()

    def connexGraph(self, connections):
        """ Check if graph is connex """
        nodes = [i for i in range(self.numVertex)]

        nodesInConnections = []
        for connection in connections:
            node1, node2 = connection
            nodesInConnections.append(node1)
            nodesInConnections.append(node2)

        if (set(nodes).difference(set(nodesInConnections))):
            return False
        return True

    def getSolution(self):
        """implement the solution here"""
        pass


if __name__ == "__main__":
    graph = Graph(5, 6, ["red", "blue", "green"])
    graph.buildEdges()
    graph.drawGraph()
