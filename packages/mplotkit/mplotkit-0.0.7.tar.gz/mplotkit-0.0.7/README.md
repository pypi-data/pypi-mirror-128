# PlotKit

Collection of some helpers and functions, mostly used by [martok](https://github.com/martok).


## Installation

Install using pip:

```pip install mplotkit```

## Usage

Minimal example:

```python
import numpy as np
import plotkit.plotkit as pk

pk.set_style('print')

fig, (ax1, ax2) = pk.new_regular(1,2)
t = np.arange(0.0, 2.0, 0.01)
ax1.plot(t, 1 + np.sin(2*np.pi*t))
pk.set_grid(ax1)
ax2.plot(t, 1 + np.cos(2*np.pi*t))
pk.set_ticks(ax2)
pk.set_grid(ax2)
pk.finalize(fig, 'example_output.png')
```
Result:
![Example Output](https://raw.githubusercontent.com/martok/py-plotkit/master/doc/example_output.png)


