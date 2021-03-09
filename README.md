# SPQ
Simple Physical Quantities for Python - Unit conversions made easy

## The name of the game

SPQ is a small python package for working easily with physical quantities and different units, with the goal of having a **compact** interface and an **easy** way of defining units.

```python
>>> from spq import Dist
>>> a = Dist.fromft(3.3)
>>> a
1.00584
>>> a.km
0.00100584
```

A physical quantity has factory methods to initialize the quantity from any of the defined units. The units are accessible as attributes of the quantity, resulting in a compact interface. No "convert_to", no strings needed - just ask for the value in the wanted unit directly.

Internally the value of the quantity is expressed in the main unit (e.g. _m_ for distance). You can use the variable to feed them into any function and perform calculations: this way the computations will be consistent. If you like, you can convert a variable to another unit for your output. Or you can use the package to perform quick unit conversions. It works with numpy arrays, too.

```python
>>> Dist.fromkm(np.linspace(1,5,5)).m
array([1000., 2000., 3000., 4000., 5000.])
```

See more examples below.

## Installation and loading

Currently there is no proper installation method. Clone the git repository to have the files in your system:

```
$ git clone git://github.com/ketakopter/spq.git
```

Add the directory to the Python path and you can import all the symbols for interactive work. This will load all the defined physical quantities.

```python
from spq import *
```

Of course, you can also load the physical quantities explicitly: 

```python
from spq import Dist, Vel
```

### Available physical quantities/units

The definition of physical quantities and units is fully specified in a json file. The best is to inspect [the file](spq/pq-aero.json). At runtime, you can also see the available units of a physical quantity with the `_units` attribute:

```python
>>> Dist._units
['m', 'ft', 'km', 'nm', 'mi', 'inch']
```

If you want to know what is the "working" unit of a physical quantity, inspect the `_mainUnit` attribute:

```python
>>> Dist._mainUnit
'm'
```

### Loading custom physical quantities/units

You can specify physical quantities and units at runtime, but the easiest is to have the definitions in a json file. Currently the way of specifying a non-default file is to set the `SPQFILE` environment variable before loading the package:

```python
# If not done prior to starting python.
import os
os.environ["SPQFILE"] = "/path/to/file"

from spc import *
```

To know more about how to define physical quantities and units, see below.

## Examples

The most basic stuff is converting scalars.

```python
>>> a = Dist(34)
>>> a.ft
111.54855643044618

>>> b = Dist.fromft(15000)
>>> b
4572.0
>>> b.ft
14999.999999999998
```

It works with numpy arrays too, and the array is converted easily to the desired units:

```python
>>> import numpy as np
>>> b = Dist.fromft(np.linspace(1,5,5))
>>> print(b)
[0.3048 0.6096 0.9144 1.2192 1.524 ]
>>> print(b.km)
[0.0003048 0.0006096 0.0009144 0.0012192 0.001524 ]
```

You can start variables from the units you want, and use the variables in functions that expect a consistent set of units, like SI:

```python
>>> def earthGravForce(m, r):
...   mu = 3.986e14  # in m3/s2
...   return mu*m/r**2

>>> m = Mass.fromlb(23)
>>> r = Dist.frommi(5000)
>>> earthGravForce(m, r)
64.22337018599708

>>> earthGravForce(10.43262, 8046720.0) # if we had input the values in kg and m directly. Same result, disregarding inaccuracies in the inputs.
64.22334242237929
```

And many more functionalities to make working with units really easy. You can find more examples in the [examples](examples) directory.

If you would like to try it live, try with the following Ipython notebook:

* [Showcase](examples/Spq_showcase.ipynb) - [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ketakopter/spq/HEAD?filepath=examples%2FSpq_showcase.ipynb) - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ketakopter/spq/blob/main/examples/Spq_showcase.ipynb)

## Requirements

SPQ works with Python 3 (tested with Python 3.6). The only needed dependency is Numpy (tested with Numpy 1.19).

