import unittest

from spq.base.gr import graphOfLinearScaling

class TestLinearGraph(unittest.TestCase):

    def test_init(self):

        factors = [('km', 'm', 1.e3), ('m', 'ft', 3.28)]

        dist_graph = graphOfLinearScaling(factors)

        self.assertEqual(dist_graph.findPath("km", "ft"), ['km', 'm', 'ft'])
