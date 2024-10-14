import sys
import os

from spq.base.pq import createPqsFromJsonFile

# Load magnitudes from external Json.
pqFile = os.environ.get('SPQFILE', None)
if not pqFile:
    raise KeyError("SPQFILE environment variable not set")
pqObjs = createPqsFromJsonFile(pqFile)

# Add the symbols to the package.
thismodule = sys.modules[__name__]
__all__ = []
for pq in pqObjs:
    setattr(thismodule, pq._name, pq)
    __all__.append(pq._name)
