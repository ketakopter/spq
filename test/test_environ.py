from pathlib import Path
import unittest
import os

curr_dir = Path(__file__).parent
res_dir = curr_dir.joinpath('resources')
test_file = res_dir.joinpath('units.json')

class TestImports(unittest.TestCase):

    def test_vol(self):

        os.environ["SPQFILE"] = str(test_file.resolve())

        from spq.spq.environ import Dist, Vol

        self.assertAlmostEqual(Vol.fromamphora(10).congius, 80.0)

    def test_noenv(self):

        def import_it():
            from spq.spq.environ import Dist, Vol

        self.assertRaises(KeyError, import_it)
