"""Market-model event-study engine (vectorised over firms) + plotting style."""
import numpy as np, pandas as pd
from common import *
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
BLUE, ORANGE, AQUA, INK, MUTED, SURF = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#c9c8c2",
    "axes.grid": True, "grid.color": "#e8e7e2", "grid.linewidth": 0.6, "axes.axisbelow": True,
    "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold", "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK, "lines.linewidth": 2,
    "legend.frameon": False, "figure.dpi": 150})

R = returns_wide()
_ix = indices().reindex(R.index)
MKT = _ix["NIFTY500"].fillna(_ix["NIFTY50"]).fillna(R.mean(axis=1))   # 18 holiday-mismatch days
DATES = R.index
EST = (-250, -30)

def t0_of(date):
    return int(np.searchsorted(DATES.values, np.datetime64(pd.Timestamp(date))))

def ar_matrix(t0, pre=10, post=60, min_obs=120):
    """Abnormal returns for all firms, rows = event days pre..post. NaN firm if thin est window."""
    a, b = t0 + EST[0], t0 + EST[1]
    if a < 0 or t0 + post >= len(DATES): return None
    y, m = R.iloc[a:b], MKT.iloc[a:b]
    ok = y.notna().sum() >= min_obs
    mc = m - m.mean()
    beta = (y.sub(y.mean())).mul(mc, axis=0).sum() / ((y.notna()).mul(mc ** 2, axis=0).sum())
    alpha = y.mean() - beta * m.mean()
    w = R.iloc[t0 - pre:t0 + post + 1]
    ar = w - (alpha.values[None, :] + np.outer(MKT.iloc[t0 - pre:t0 + post + 1].values, beta.values))
    ar = ar.loc[:, ok]; ar.index = range(-pre, post + 1)
    return ar

def car(ar, lo, hi):
    x = ar.loc[lo:hi]
    return x.sum(min_count=max(1, int(0.7 * (hi - lo + 1))))

WINDOWS = [(-1, 1), (0, 5), (0, 10), (0, 20), (0, 40)]

def placebo_t0s(n=1000, seed=7, post=60):
    rng = np.random.default_rng(seed)
    lo, hi = -EST[0] + 5, len(DATES) - post - 1
    return rng.integers(lo, hi, n)
