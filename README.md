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

## Examples

See the examples directory.



