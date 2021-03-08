# SPQ
Simple Physical Quantities for Python - Unit conversions made easy

## The name of the game

SPQ is a small python package for working easily with physical quantities and different units, with the goal of having a **compact** interface and an **easy** way of defining units.

```python
>>> from spq import Dist
>>> a = Dist.fromft(3.3)
>>> a
1.0058399984711233
>>> a.km
0.0010058399984711232
```

The idea is that a physical quantity is initialized from whatever unit, and it is converted to the main unit (e.g. meters for distance). You can use the variable to feed them into any function and perform calculations: this way the computations will be consistent. If you like, you can convert a variable to another unit for your output. Or you can use the package to perform quick unit conversions. It works with numpy arrays, too.

```python
>>> Dist.fromkm(np.linspace(1,5,5)).m
array([1000., 2000., 3000., 4000., 5000.])
```

See more examples below.

## Installation and loading

Currently there is no proper installation method. Clone the git repository to have the files in your system:

```
git clone git://github.com/ketakopter/spq.git
```

Add the directory to the Python path and you can import the package as usual. 

```python
from spq import Dist, Vel
```

For quick use in Ipython sessions, you can import all from the package (you don't have to type all the quantities you are going to use and you don't have to type the prefix):

```python
from spq import *
```

### Choosing the physical quantities/units to be used

The package loads the definitions of physical quantities and units from a json file. Currently only one file is supported, which loads typical units used in aerospace (ft, kt...) and the main units are the SI units (m, m/s...).

You can specify a different file to be used by setting an environment variable previous to loading the package:

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
111.54855660000001

>>> b = Dist.fromft(15000)
>>> b
4571.99999305056
>>> b.ft
15000.0
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

>>> earthGravForce(10.43262, 8046720.0)
64.22334242237929
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

And many more functionalities to make working with units really easy. You can find more examples in the [examples](examples) directory.

If you would like to try it live, try with the following Ipython notebook:

* [Showcase](examples/Spq_showcase.ipynb) - [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ketakopter/spq/HEAD?filepath=examples%2FSpq_showcase.ipynb) - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ketakopter/spq/blob/main/examples/Spq_showcase.ipynb)



