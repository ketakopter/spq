import unittest
from pathlib import Path

import numpy as np

from spq.base.gr import Gr, graphOfLinearScaling
from spq.base.pq import createPq, createPqFromDict, createPqsFromJsonFile

curr_dir = Path(__file__).parent
res_dir = curr_dir.joinpath('resources')
test_file = res_dir.joinpath('units.json')

class TestSpqCreation(unittest.TestCase):

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

    def test_dict(self):

        dct = {'name': 'Dist',
               'description': 'distance',
               'main_unit': 'm',
               'conversions': [
                   {'from': 'm', 'to': 'ft', 'factor': 3.28},
                   {'from': 'km', 'to': 'm', 'factor': 1000.0},
                   {'from': 'sm', 'to': 'm', 'factor': 1.0, 'origin': 500.0}
               ]
               }

        Dist = createPqFromDict(dct)

        self.assertAlmostEqual(Dist.fromft(3.28), 1)
        self.assertAlmostEqual(Dist.fromft(3.28).km, 1e-3)
        self.assertAlmostEqual(Dist.fromsm(0), 500.0)
        self.assertAlmostEqual(Dist(0).sm, -500.0)
        self.assertAlmostEqual(Dist.fromkm(1).sm, 500.0)

    def test_json(self):

        pqs = createPqsFromJsonFile(test_file)

        self.assertEqual(sorted([q._name for q in pqs]), ['Dist', 'Vol'])

        Dist, Vol = pqs

        self.assertEqual(sorted(Dist._units), ['digitus', 'palmus', 'passus', 'pes', 'stadium'])
        self.assertEqual(sorted(Vol._units), ['amphora', 'congius', 'quartarius'])

        a = Dist.frompes(1)

        self.assertAlmostEqual(a.digitus, 16.0)
        self.assertAlmostEqual(a.palmus, 4.0)
        self.assertAlmostEqual(a.pes, 1.0)
        self.assertAlmostEqual(a.passus, 0.2)
        self.assertAlmostEqual(Dist.frompassus(1).digitus, 80.0)

        b = Vol.fromamphora(10)

        self.assertAlmostEqual(b.congius, 80.0)
        self.assertAlmostEqual(b.quartarius, 1920.0)
