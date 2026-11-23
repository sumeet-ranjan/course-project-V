"""SUPERSEDED 22 Nov 2026: result withdrawn (the scaffold links are unverified industry guesses).
Indirect (supply-chain) propagation using the pack's INDUSTRY-LEVEL scaffold (hypotheses only).
For each event: firms with <5% of assets in the zone are split into 'linked' (scaffold supplier
or buyer of a firm with >=25% of assets in the zone) and 'unlinked'. Placebo-date p-values."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
sc = pd.read_csv(D + "supply_chain_scaffold.csv"); ex = exposure(); PL = placebo_t0s(500)
WIN = [(0, 5), (0, 10), (0, 20), (0, 40)]
def groups(zone, firms):
    s = ex[ex.zone == zone].set_index("nse_symbol").share_cost.reindex(firms).fillna(0)
    hit = set(s[s >= .25].index); clean = set(s[s < .05].index)
    up = set(sc.supplier[sc.buyer.isin(hit)]) & clean      # suppliers of hit firms (lose offtake, H3)
    dn = set(sc.buyer[sc.supplier.isin(hit)]) & clean      # buyers of hit firms (lose input, H2)
    return hit, up, dn, clean - up - dn
def stat(ar, g):
    hit, up, dn, un = g; o = {}
    for w in WIN:
        c = car(ar, *w)
        o[w] = (c.reindex(list(up)).mean() - c.reindex(list(un)).mean(), c.reindex(list(dn)).mean() - c.reindex(list(un)).mean())
    return o
rows = []
for z in ["NCR", "GJ", "HP", "CHE"]:
    g = groups(z, R.columns)
    pl = [stat(a, g) for a in (ar_matrix(int(t)) for t in PL) if a is not None]
    for _, e in EVENTS[EVENTS.zone == z].iterrows():
        s = stat(ar_matrix(t0_of(e.start)), g)
        for w in WIN:
            for k, nm, grp in [(0, "suppliers of hit firms (upstream)", g[1]), (1, "buyers of hit firms (downstream)", g[2])]:
                if len(grp) < 2: continue
                d = np.array([p[w][k] for p in pl])
                rows.append(dict(event=e.label, link=nm, n_linked=len(grp), n_unlinked=len(g[3]), n_hit=len(g[0]), window=f"[{w[0]},{w[1]}]",
                                 car_linked_minus_unlinked=s[w][k], p_placebo=np.mean(np.abs(d - d.mean()) >= abs(s[w][k] - d.mean())),
                                 linked_firms="|".join(sorted(grp))))
r = pd.DataFrame(rows); r.to_csv(TAB + "propagation_scaffold.csv", index=False)
pd.set_option("display.width", 220); print(r.drop(columns="linked_firms").round(4).to_string())
print(r.groupby("link").linked_firms.first().to_dict())
