# SPQ
Simple Physical Quantities for Python - Unit conversions made easy

## The name of the game

SPQ is a small python package for working easily with physical quantities and different units, with
the goal of having a **compact** interface and an **easy** way of defining units.

```python
>>> from spq.spq.aero import Dist
>>> a = Dist.fromft(3.3)
>>> a
1.00584
>>> a.km
0.00100584
```

A physical quantity has factory methods to initialize the quantity from any of the defined units,
resulting in a functional interface. The units are accessible as attributes of the quantity,
resulting in a compact interface. No "convert_to", no strings needed - just ask for the value in the
wanted unit directly.

Internally the value of the quantity is expressed in the main unit (e.g. _m_ for distance). You can
use the variable to feed them into any function and perform calculations: this way the computations
will be consistent. If you like, you can convert a variable to another unit for your output. Or you
can use the package to perform quick unit conversions. It works with numpy arrays, too.

```python
>>> Dist.fromkm(np.linspace(1,5,5)).m
array([1000., 2000., 3000., 4000., 5000.])
```

SPQ provides physical quantities and units in isolated modules. Instead of having a library to
handle all imaginable units, each application will define and/or load their needed definitions.
Ready-to-use modules are provided in the **spq** sub-package. If you want to create your own
definitions, you can use the functionalities of the **base** sub-package. See examples and
instructions below.


## Examples

The most basic stuff is using one of the physical quantities to input and show
the quantity in the units that you want.

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

You can start variables from the units you want, and use the variables in functions that expect a
consistent set of units, like SI:

```python
>>> from spq.spq.aero import Dist, Mass

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

And many more functionalities to make working with units really easy. You can find more examples in
the [examples](examples) directory.

If you would like to try it live, try with the following Ipython notebook:

* [Showcase](examples/Spq_showcase.ipynb) - [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ketakopter/spq/HEAD?filepath=examples%2FSpq_showcase.ipynb) - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ketakopter/spq/blob/main/examples/Spq_showcase.ipynb)


## Installation

You can install the package from PyPi:

``` shell
$ pip install spq
```

Otherwise, clone the git repository to have the files in your system and install with pip:

``` shell
$ git clone git://github.com/ketakopter/spq.git
$ cd spq
$ pip install .
```


## Loading physical quantities

SPQ is organized in modules that contain the definitions of units and physical quantities. Currently
the *aero* module is available for users.

```python
from spq.spq.aero import Dist, Vel
```

The definition of physical quantities and units is fully specified in a json file. The best is to
inspect [the file](spq/spq/pq-aero.json).

### Loading custom physical quantities/units

The *environ* module lets one load the definitions from a file defined in the `SPQFILE` environment
variable, following the same syntax as the file above.

``` python
import os
os.environ['SPQFILE'] = '/path/to/file'
from spq.spq.environ import Dist, Mass
```

You can build your own module using the functionalities of the `spq.base` package. This lets you
define units and conversions in a variety of ways: from a json file, dictionary of units, or a
custom graph. The best is to inspect how the `spq.spq.aero` module loads the definitions, and check
the [example notebook](examples/Spq_creation_examples.ipynb). You can also try it live: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ketakopter/spq/HEAD?filepath=examples%2FSpq_creation_examples.ipynb) - [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ketakopter/spq/blob/main/examples/Spq_creation_examples.ipynb)


### Available units

At runtime, you can see the available units of a physical
quantity with the `_units` attribute:

```python
>>> Dist._units
['m', 'ft', 'km', 'nm', 'mi', 'inch']
```

If you want to know what is the "working" unit of a physical quantity, inspect the `_mainUnit` attribute:

```python
>>> Dist._mainUnit
'm'
```

## What SPQ is, and what is not

The goal of SPQ was to be able to quickly work with quantities and output results in different
units, especially for interactive work. The variables derive from `float` and `np.ndarray` to be
able to feed them to existing functions, and the value is internally stored in SI units (by default)
in order to have consistent computations. The idea was to work with numerical values, no strings
needed. Having the units as attributes makes it really easy to write the output in the wanted units
or plot them, like `plt.plot(x.mi, y.mph)`.

Also, the definition of physical quantities and units should be easy. The json file defining the
defaults was easy to prepare and extending it is immediate.

SPQ allows to have definitions for each application. It is **not** meant to be a library that
handles all the imaginable units. The functionalities allow to have independent definitions, that
are best tailored for each application.

SPQ is **not** intended to be a full-fledged physical quantities library, like when you multiply a
length by a force you get a torque (or an energy...). Doing that would need to define relationships
between physical quantities, define how operators work, and it would over-complicate the library for
the intended use. Doing computations with SPQ objects just results in floats or arrays; it's up to
the user to initialize whatever physical quantity with the results.

## Requirements

SPQ works with Python 3 (tested with Python 3.7 and 3.12). The only needed dependency is Numpy.
