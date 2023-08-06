from math import pi, log10, ceil
from typing import Optional, Dict

import numpy as np
import plotkit.plotkit as pk
from sympy import Expr, sympify, Symbol


def plot_system(transfer: Expr, fmin: float = 1, fmax: float = 100000,
                amplitude_linear: bool = False,
                points_per_decade: int = 50,
                values: Optional[Dict[str, float]] = None,
                return_fig=False) -> Optional[pk.Figure]:
    if values is None:
        values = {}

    rvals = {Symbol(n): sympify(v) for n, v in values.items()}
    rexpr: Expr = transfer.xreplace(rvals)

    s = Symbol("s")

    def feval(w: complex) -> complex:
        v = rexpr.evalf(subs={s: w})
        if v.free_symbols:
            raise ValueError("Some symbols not given values: " + str(v.free_symbols))
        return complex(v)

    points = ceil(log10(fmax / fmin) * points_per_decade)
    X = np.geomspace(fmin, fmax, points)
    Xiw = X * 2 * pi * 1j
    Y = np.array([feval(iw) for iw in Xiw], dtype=np.cfloat)

    if amplitude_linear:
        ampl = np.abs(Y)
    else:
        ampl = 20 * np.log10(np.abs(Y))
    phase = np.angle(Y, deg=True)

    fig, (ax, ax2) = pk.new_regular(2, 1)

    pk.set_grid(ax)
    if amplitude_linear:
        ax.set_ylabel("Amplitude")
    else:
        ax.set_ylabel("Amplitude / dB")
    ax.semilogx(X, ampl)
    ax.set_xlim(fmin, fmax)
    pk.set_grid(ax2)
    ax2.set_ylabel("Phase / °")
    ax2.set_xlabel("Frequency / Hz")
    ax2.semilogx(X, phase)
    ax2.set_xlim(fmin, fmax)
    if return_fig:
        return fig
    pk.finalize(fig)
