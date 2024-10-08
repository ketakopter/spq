import unittest

import numpy as np

from spq.gr import Gr
from spq.spq import createPq

class TestGraph(unittest.TestCase):

    def test_graph(self):

        def m2ft(m):
            return m / 0.3048
        def ft2m(ft):
            return ft * 0.3048
        def m2km(m):
            return m / 1e3
        def km2m(km):
            return km * 1e3

        dist_graph = Gr()
        dist_graph.addEdge('m', 'ft', m2ft)
        dist_graph.addEdge('ft', 'm', ft2m)
        dist_graph.addEdge('m', 'km', m2km)
        dist_graph.addEdge('km', 'm', km2m)
        dist_graph.addEdge('m', 'expm', lambda m: np.exp(m))
        dist_graph.addEdge('expm', 'm', lambda expm: np.log(expm))

        Dist = createPq(dist_graph, 'm')

        self.assertAlmostEqual(Dist(4.1), 4.1)
        self.assertAlmostEqual(Dist(4.1).ft, 13.451443569553804)
        self.assertAlmostEqual(Dist.fromft(3.53), 1.075944)
        self.assertAlmostEqual(Dist.fromft(3.53).m, 1.075944)
        self.assertAlmostEqual(Dist.fromft(3.53).ft, 3.53)
        self.assertAlmostEqual(Dist.fromft(3.53).km, 0.001075944)
        self.assertAlmostEqual(Dist.fromexpm(3).m, np.log(3))
        self.assertAlmostEqual(Dist(2).expm, np.exp(2))
