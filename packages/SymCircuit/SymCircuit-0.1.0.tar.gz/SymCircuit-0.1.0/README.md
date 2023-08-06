# SymCircuit

Provides classes to do electronic circuit analysys using symbolic equations. For example,
it is possible to automatically find equations using Kirchhoff's laws and solve them for specific
properties.

As a bonus, the equation solving part can be used independently of the rest.

## Installation

Minimal install using pip (just the equation solver):

```pip install SymCircuit```

Full install using pip:

```pip install SymCircuit[EE]```


## Usage

For more detailed examples, see the files in directory `examples/`.

Example of using a netlist for a random arrangement of elements:

```python
from io import StringIO

import plotkit.plotkit as pk

from symcircuit.bode import plot_system
from symcircuit.spice import Circuit
from symcircuit.system import SymbolicSystem

circ = Circuit()
circ.parse_spice_netlist(StringIO(r"""
* examples\network1.asc
R1 N001 0 1k
R2 N002 0 3k
C1 N002 0 50µ
L1 N001 N002 120µ
V1 N001 0 AC 1
.ac dec 30 10 10000
.backanno
.end
"""))

# translate to equation system
s = SymbolicSystem(circ.to_system_description())

# Add "measurement" characteristics
s.extend(SymbolicSystem("""
Zsys == V1 / i_V1
"""))
print(s.info())

# find transfer function
impedance = s.focus("Zsys")["Zsys"]
print("System Impedance = ", impedance)
# System Impedance =  -R1*(C1*L1*R2*s**2 + L1*s + R2)/(C1*L1*R2*s**2 + L1*s + R1*(C1*R2*s + 1) + R2)

# plot parameterised transfer function
v = dict(
    R1=1e3,
    R2=3e3,
    C1=50e-6,
    L1=120e-6,
)
fig = plot_system(impedance, 10, 50000, values=v, amplitude_linear=True, return_fig=True)
pk.finalize(fig)
```
Result:
![Example Output](https://raw.githubusercontent.com/martok/py-symcircuit/main/doc/impedance_plot.png)

## Credits:

* [NetworkX](https://networkx.org/) is used for graph analysis
* The `focus` and `seek` methods are based on the implementation proposed by Christopher Smith @smichr in [a sympy issue](https://github.com/sympy/sympy/issues/2720#issuecomment-312437508).
