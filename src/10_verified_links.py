"""SUPERSEDED 22 Nov 2026: result withdrawn (wrong NCR hit firms; Petronet shock unconfirmed; Aarti-UPL JV not live).
Use src/40_links_file.py and outputs/deliverables/verified_links.csv instead.
Propagation along VERIFIED firm-to-firm links (research/verified_links_*.csv) instead of the
pack's industry scaffold. Too few links for a regression -> case table: for each link whose one
end sits in an event zone, the other end's abnormal return vs unexposed firms, with that firm's
own placebo-date percentile."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from es_lib import *
L = pd.concat([pd.read_csv(ROOT + "/research/verified_links_chemicals_gas_steel.csv"), pd.read_csv(ROOT + "/research/verified_links_tyres_auto_ncr.csv")])
L["supplier_symbol"] = L.supplier_symbol.astype(str).str.split().str[0]
L.to_csv(ROOT + "/research/verified_links_all.csv", index=False)
ins = L[L.in_sample.astype(str).str.lower().eq("true") & L.supplier_symbol.isin(R.columns) & L.buyer_symbol.isin(R.columns)]
ins = ins[~ins["product"].str.contains("NOT a supply|equity link|corroboration", case=False)].drop_duplicates(["supplier_symbol", "buyer_symbol"])
print(ins[["supplier_symbol", "buyer_symbol", "product", "dependence_value", "evidence_strength"]].to_string())
ex = exposure(); PL = placebo_t0s(500); rows = []
PAR = {int(t): ar_matrix(int(t), pre=1, post=25) for t in PL}
for _, e in EVENTS[EVENTS.src != "pack"].iterrows() if False else EVENTS[EVENTS.event_id != "E_NCR_GRAP_2024"].iterrows():
    s = ex[ex.zone == e.zone].set_index("nse_symbol").share_cost
    un = [c for c in R.columns if s.get(c, 0) == 0]
    ar = ar_matrix(t0_of(e.start), pre=1, post=25)
    for _, l in ins.iterrows():
        for hit, other, role in [(l.supplier_symbol, l.buyer_symbol, "buyer of hit supplier"), (l.buyer_symbol, l.supplier_symbol, "supplier of hit buyer")]:
            if s.get(hit, 0) < .25 or other not in ar: continue
            d = dict(event=e.label, hit_firm=hit, hit_share=round(s.get(hit, 0), 2), linked_firm=other, role=role, linked_own_share=round(s.get(other, 0), 2),
                     product=l["product"][:60], dependence=l.dependence_value, evidence=l.evidence_strength)
            for h in (5, 10, 20):
                v = ar[other].loc[0:h].sum() - ar[[c for c in un if c in ar]].loc[0:h].sum().mean()
                pl = np.array([a[other].loc[0:h].sum() - a[[c for c in un if c in a]].loc[0:h].sum().mean() for a in PAR.values() if a is not None and other in a])
                d[f"adj_car_0_{h}"] = v; d[f"placebo_pctile_0_{h}"] = (pl < v).mean()
            rows.append(d)
r = pd.DataFrame(rows); r.to_csv(TAB + "propagation_verified_links.csv", index=False)
pd.set_option("display.width", 250); print(r.drop(columns=["product", "dependence", "evidence"]).round(3).to_string())
print("mean adj CAR[0,10] across cases:", r.adj_car_0_10.mean().round(4), " share negative:", (r.adj_car_0_10 < 0).mean().round(2), " n:", len(r))
