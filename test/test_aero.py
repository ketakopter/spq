import unittest

import numpy as np

from spq.spq.aero import Dist, Dens, Vel, Vol, Temp, Press, Power, Mass, Ang, Area, Force, Weight, Angv, Flow, FlowD

class TestImports(unittest.TestCase):

    def test_imports(self):

        self.assertAlmostEqual(Vel.fromkt(200), 102.888)
