class Gr(object):
    """
    Rough implementation of Graphs, not robust.

    """

    def __init__(self):
        self.nodes = []
        self.connections = {}
        self.neighbours = {}

    def addNode(self, node):
         self.nodes.append(node)

    def addEdge(self, node1, node2, edge):
        """Adds a connection between node1 and node2. The nodes do not need to
           exist, they will be added to the graph if needed."""
        if node1 not in self.nodes:
            self.nodes.append(node1)
        if node2 not in self.nodes:
            self.nodes.append(node2)
        if node1 in self.neighbours.keys():
            self.neighbours[node1].append(node2)
        else:
            self.neighbours[node1] = [node2]
        self.connections[(node1, node2)] = edge

    def findPath(self, startNode, endNode, path=[]):
        """
        Find a path from startNode to endNode in graph. This is only the
        path (list of nodes), which can be used to get the edges.

        From https://www.python.org/doc/essays/graphs/.

        """
        path = path + [startNode]
        if startNode == endNode:
            return path
        if startNode not in self.neighbours:
            return None
        for node in self.neighbours[startNode]:
            if node not in path:
                extended_path = self.findPath(node, endNode, path)
                if extended_path: return extended_path
        return None

    def getEdges(self, path):
        return [self.connections[(path[i],path[i+1])] for i in range(len(path)-1)]
