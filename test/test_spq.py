import unittest

import numpy as np

from spq import Dist

class TestDist(unittest.TestCase):

    def test_dist(self):

        a = Dist(34)

        self.assertAlmostEqual(34.0, a)
        self.assertAlmostEqual(0.034, a.km)
        self.assertAlmostEqual(111.54855643, a.ft)

    def test_dist_from(self):

        b = Dist.fromft(15000)

        self.assertAlmostEqual(4572.0, b)
        self.assertAlmostEqual(4572.0, b.m)
        self.assertAlmostEqual(15000.0, b.ft)

    def test_numpy(self):

        c = Dist.fromft(np.arange(0, 31000, 10000))

        np.testing.assert_array_almost_equal(c, [0.0, 3048.0, 6096.0, 9144.0])
        np.testing.assert_array_almost_equal(c.m, [0.0, 3048.0, 6096.0, 9144.0])
        np.testing.assert_array_almost_equal(c.ft, [0., 10000., 20000., 30000.])

    def test_numpy_filter(self):

        f = Dist.fromft(np.arange(1, 10))

        np.testing.assert_array_almost_equal(f.m, [0.3048, 0.6096, 0.9144, 1.2192, 1.524, 1.8288, 2.1336, 2.4384, 2.7432])
        np.testing.assert_array_almost_equal(f[f > 1], [1.2192, 1.524, 1.8288, 2.1336, 2.4384, 2.7432])
        np.testing.assert_array_almost_equal(f[f.ft > 2], [0.9144, 1.2192, 1.524, 1.8288, 2.1336, 2.4384, 2.7432])
        np.testing.assert_array_almost_equal(f[f.ft > 2].ft, [3., 4., 5., 6., 7., 8., 9.])
        np.testing.assert_array_almost_equal(f[f > Dist.fromft(2)].ft, [3., 4., 5., 6., 7., 8., 9.])

    def test_numpy_element(self):

        g = Dist.fromft(np.arange(1,10))
        g_e = g[3]
        np.testing.assert_array_almost_equal(g_e, 1.2192)
        np.testing.assert_array_almost_equal(g_e.ft, 4.0)
