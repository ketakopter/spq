import sys
import os

from spq.base.pq import createPqsFromJsonFile

# Load magnitudes from external Json.
pqFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),'pq-aero.json')
pqObjs = createPqsFromJsonFile(pqFile)

# Add the symbols to the package.
thismodule = sys.modules[__name__]
__all__ = []
for pq in pqObjs:
    setattr(thismodule, pq._name, pq)
    __all__.append(pq._name)
