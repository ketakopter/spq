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

def _buildLinearScalerFunctions(factor, origin=0.0):
    def a2b(a):
        return origin + factor*a
    def b2a(b):
        return -(origin/factor) + (1./factor)*b
    return a2b, b2a

def graphOfLinearScaling(factors):
    """Builds a graph based on linear scaling. Only the one-way factors need to be given, the
    reverse factors are constructed by reversing the linear scaling.

    The scaling is done as y = A + B*x = origin + factor*x. The reverse scaling is done with
    x = -(origin/factor) + (1./factor)*y.

    The factors are given as a list of tuples (the origin is optional and defaults to 0):

    [ (from, to, factor), (from, to, factor, origin), ...]

    e.g.:

    [('km', 'm', 1.e3), ('m', 'ft', 3.28)]

    The results is a graph which contains units as nodes and functions at the edges, such
    that if e.g. the edge from 'm' to 'ft' is used, the edge is a function that performs
    f(x): x*3.28.

    An example for temperature:

    [('c', 'f', 1.8,  32), ('c', 'k', 1.0, 273.15)]

    """

    graph = Gr()
    for f in factors:
        frm    = f[0]
        to     = f[1]
        factor = f[2]
        origin = f[3] if len(f)==4 else 0.0
        frm2to, to2frm = _buildLinearScalerFunctions(factor, origin)

        graph.addEdge(frm, to, frm2to)
        graph.addEdge(to, frm, to2frm)

    return graph
