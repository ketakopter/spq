import unittest

from spq import Dist

class TestSpq(unittest.TestCase):

    def test_dist(self):

        a = Dist(34)

        self.assertAlmostEqual(34.0, a)
        self.assertAlmostEqual(0.034, a.km)
        self.assertAlmostEqual(111.54855643, a.ft)
