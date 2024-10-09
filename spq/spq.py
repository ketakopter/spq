"""
SPQ - Simple Physical Quantities - Unit conversions made easy
=============================================================

The module provides the functionalities to create Physical Quantity (Pq) objects, which
have the ability to handle different units. A Physical Quantity has a main unit. When
initializing a variable, the input value is converted to that unit. When asking for the
value, it is converted to the desired unit.

The basic way of creating a Pq is with a graph with unit conversions. A graph contains
units at the nodes, and conversion functions at the edges. The module provides a
function to create a complete graph based on one-directional conversions (it
automatically creates the inverse conversions).

For example, to create a distance Pq, we can define conversions between different units,
create a graph, and create the Pq:

>>> distUnits = [('m', 'ft', 3.2808399),
...              ('km', 'm', 1.e3, 0.0),
...              ('nm', 'm', 1852.),
...              ('mi', 'm', 1609.344)]
>>> distGraph = graphOfLinearScaling(distUnits)
>>> Dist = createPq(distGraph, 'm')

Note that we don't need to specify *all* conversions. As long as the graph is strongly
connected, it works. See the `graphOfLinearScaling` docstring for info on what is
expected from the units conversions and how the graph is generated.

You can also create your own graph with the wanted functions at the edges:

>>> from .gr import Gr
>>> tempGraph = Gr()
>>> tempGraph.addEdge('c', 'f', lambda c: c*1.8 + 32)
>>> tempGraph.addEdge('f', 'c', lambda f: (f-32.0)/1.8)
>>> tempGraph.addEdge('c', 'k', lambda c: c + 273.15)
>>> tempGraph.addEdge('k', 'c', lambda k: k - 273.15)
>>> Temp = createPq(tempGraph, 'k')

Further functionalities include creating a Pq from a dict (see `createPqFromDict`) and
loading several Pqs from a Json file (see `createPqsFromJsonFile`).

Once you have a Pq, you can initialize it with any of the units, and request the value
also in any of the units (if not specified, the default is the main unit):

>>> Dist(34)
34.0
>>> Dist.fromft(15)
4.57199999305056
>>> Dist.fromft(15).km
0.00457199999305056
>>> Dist.fromft(15).ft
15.0

"""

from .gr import graphOfLinearScaling
import numpy as np
import json

def _buildRecursiveClassmethod(funcList):
    def a2c(cls, a):
        x = a
        for f in funcList:
            x = f(x)
        return cls(x)
    return a2c

def _buildRecursiveProperty(funcList):
    def a2c(self):
        x = self
        for f in funcList:
            x = f(x)
        return x
    return a2c

def _buildFactorySetter(ScalarPq, unit):
  def fs(cls,a):
    return cls(np.asarray([getattr(ScalarPq,'from'+unit)(x) for x in np.asarray(a).flatten()]).reshape(np.asarray(a).shape))
  return fs

def _buildPropertySetter(unit):
  def prop(self):
    return np.asarray([getattr(x, unit) for x in self.flatten()]).reshape(self.shape)
  return prop

def _buildSupraFactory(ScalarPq, VectorPq, unit):
  def fs(cls, a):
    return getattr(VectorPq, 'from'+unit)(a) if isinstance(a, (list, tuple, np.ndarray)) else getattr(ScalarPq, 'from'+unit)(a)
  return fs


class _VectorPqBase(np.ndarray):
  """
  Only used to identify VectorPqs for transforming them for ufuncs (see below).
  """
  pass

def createPq(graph, mainUnit, name=None):
  """
  graph is a graph with units at the nodes (strings) and conversion functions at the
  edges. The graph is supposed to be directed and strongly connected (no check is done).
  The edge functions are of the form `to = frm2to(frm)`.

  There is a mainUnit (string), which should be present in the graph as one of the nodes.

  This function returns a class (not an instance), which contains factory methods for
  all units, and properties for all units. All the needed convertions are performed by
  navigating through the graph.

  """

  units = graph.nodes

  # Scalar pq
  class ScalarPq(float):
    pass
  for unit in [u for u in units if u != mainUnit]:
    frm = unit
    to  = mainUnit
    funcPath = graph.getEdges(graph.findPath(frm, to))
    frm2to = _buildRecursiveClassmethod(funcPath)

    setattr(ScalarPq, 'from'+unit, classmethod(frm2to))
  for unit in [u for u in units if u != mainUnit]:
    frm = mainUnit
    to  = unit
    funcPath = graph.getEdges(graph.findPath(frm, to))
    frm2to = _buildRecursiveProperty(funcPath)

    setattr(ScalarPq, unit, property(frm2to))
  setattr(ScalarPq, 'from'+mainUnit, classmethod(lambda cls,x: cls(x)))
  setattr(ScalarPq, mainUnit, property(lambda x:x))

  # Vector pq
  class VectorPq(_VectorPqBase):
    def __new__(cls, a):
      obj = np.asarray([ScalarPq(x) for x in np.asarray(a).flatten()], dtype=object).reshape(np.asarray(a).shape).view(cls)
      return obj
    #def __array_finalize__(self, obj):
      # Not needed?
      # if obj is None: return
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
      # Mix of:
      # https://numpy.org/doc/stable/reference/generated/numpy.lib.mixins.NDArrayOperatorsMixin.html#numpy.lib.mixins.NDArrayOperatorsMixin
      # and "Subclassing ndarray" doc.
      inputs = tuple(np.asarray(x, dtype=float) if isinstance(x, _VectorPqBase) else x for x in inputs)
      out = kwargs.get('out', ())
      if out:
        kwargs['out'] = tuple(np.asarray(x, dtype=float) if isinstance(x, _VectorPqBase) else x for x in out)
      results = super(VectorPq, self).__array_ufunc__(ufunc, method, *inputs, **kwargs)
      return results
  for unit in units:
    vecFactorySetter = _buildFactorySetter(ScalarPq, unit)
    setattr(VectorPq, 'from'+unit, classmethod(vecFactorySetter))
    vecPropertySetter = _buildPropertySetter(unit)
    setattr(VectorPq, unit, property(vecPropertySetter))

  # Supra pq.
  class Pq(object):
    def __new__(cls, a):
      return VectorPq(a) if isinstance(a, (list, tuple, np.ndarray)) else ScalarPq(a)
  Pq._graph    = graph
  Pq._units    = units
  Pq._mainUnit = mainUnit
  Pq._name     = name
  for unit in units:
    supraFactory = _buildSupraFactory(ScalarPq, VectorPq, unit)
    setattr(Pq, 'from'+unit, classmethod(supraFactory))

  return Pq

def createPqFromDict(pqDict):
  """
  Example of parseable dict:

  {'name': 'Dist',
   'description': 'distance',
   'main_unit': 'm',
   'conversions': [
     {'from': 'm', 'to': 'ft', 'factor': 3.2808399},
     {'from': 'km', 'to': 'm', 'factor': 1000.0},
     {'from': 'mi', 'to': 'm', 'factor': 1609.344, 'origin': 0.0}
    ]
   }
  """
  pqFactors = map(lambda c: tuple(c.get(n, 0.0) for n in ['from', 'to', 'factor', 'origin']), pqDict['conversions'])
  pqGraph   = graphOfLinearScaling(pqFactors)

  mainUnit   = pqDict['main_unit']
  name       = pqDict['name']

  return createPq(pqGraph, mainUnit, name)

def createPqsFromJsonFile(filepath):

  with open(filepath) as fp:
    jsonData = json.load(fp)

  pqs = [createPqFromDict(pqDict) for pqDict in jsonData['physical_quantities']]
  return pqs
