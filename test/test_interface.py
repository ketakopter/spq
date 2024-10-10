import unittest

import numpy as np

from spq.spq.aero import Dist

class TestInterface(unittest.TestCase):

    def test_scalar(self):

        a = Dist(34)

        self.assertAlmostEqual(34.0, a)
        self.assertAlmostEqual(0.034, a.km)
        self.assertAlmostEqual(111.54855643, a.ft)

    def test_scalar_from(self):

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

    def test_numpy_functions(self):

        h = Dist(np.arange(1,10))

        np.testing.assert_array_almost_equal(h, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
        np.testing.assert_array_almost_equal(np.sqrt(h), [1., 1.41421356, 1.73205081, 2., 2.23606798, 2.44948974, 2.64575131, 2.82842712, 3., ])
        np.testing.assert_array_almost_equal(h.km, [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009])
        np.testing.assert_array_almost_equal(np.exp(h.km), [1.0010005, 1.002002, 1.0030045, 1.00400801, 1.00501252, 1.00601804, 1.00702456, 1.00803209, 1.00904062])

    def test_numpy_broadcasting(self):

        i = Dist([[3,4],[8,9]])
        j = np.array([4,5])
        np.testing.assert_array_almost_equal(i*j, [[12., 20.], [32., 45.]])

    def test_chain(self):

        self.assertEqual(Dist.fromm(1000).km, 1.0)
