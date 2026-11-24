"""Cement plants: coordinates and road distance to Delhi (checkpoint-5 review; specification in table2_notes.md).

Input: research/realign/cement_plants_A.csv, _B.csv, _C.csv (plants from original documents; collected by agents),
_D.csv (Ambuja and ACC site lists from their FY2023-24 annual reports, added by hand; all
quotes checked by src/42). Each distinct (place, district, state) is geocoded with OpenStreetMap Nominatim
(https://nominatim.openstreetmap.org, policy: <= 1 request a second, an identifying User-Agent), and checked against the
project's district centroids (external/district_centroids.csv): amended before the test was run, the geocode is kept if its
address is in the stated state and within 150 km of its district centroid; otherwise the centroid is used and the plant flagged. Road distance from Delhi (Connaught Place, 28.6315 N,
77.2167 E) comes from the OSRM public router (router.project-osrm.org; light use). Results are cached in
external/cement_geo_cache.csv so the services are asked once per place.
Outputs: outputs/deliverables/cement_plants_geo.csv (one row per plant, with lat, lon, road_km, straight_km, flags)
"""
import os, sys, json, time, math, urllib.request, urllib.parse; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd, numpy as np
from common import ROOT, EXT, OUT
RE = ROOT + "/research/realign/"; DEL = OUT + "deliverables/"
UA = {"User-Agent": "climate-project-research-script/1.0 (academic research; cement plant distances)"}
DELHI = (28.6315, 77.2167)
CACHE = EXT + "cement_geo_cache.csv"
def hav(a, b):
    R = 6371.0; p1, p2 = math.radians(a[0]), math.radians(b[0]); dp = p2 - p1; dl = math.radians(b[1] - a[1])
    return 2 * R * math.asin(math.sqrt(math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2))
def get(u):
    return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode())
def geocode(q):
    r = get("https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": q, "format": "json", "limit": 1, "countrycodes": "in"})); time.sleep(1.2)
    return (float(r[0]["lat"]), float(r[0]["lon"]), r[0].get("display_name", "")) if r else None
def route(lat, lon):
    r = get(f"https://router.project-osrm.org/route/v1/driving/{DELHI[1]},{DELHI[0]};{lon},{lat}?overview=false"); time.sleep(1.2)
    return r["routes"][0]["distance"] / 1000.0 if r.get("code") == "Ok" and r.get("routes") else np.nan
def load_plants():
    fs = [RE + f"cement_plants_{k}.csv" for k in "ABCDE" if os.path.exists(RE + f"cement_plants_{k}.csv")]
    P = pd.concat([pd.read_csv(f, dtype=str).fillna("").assign(source_file=os.path.basename(f)) for f in fs], ignore_index=True) if fs else pd.DataFrame()
    return P[P.place.astype(str).str.strip() != ""] if len(P) else P     # rows without a place are firm totals, not plants
def main(test=None):
    cache = pd.read_csv(CACHE, dtype={"key": str}) if os.path.exists(CACHE) else pd.DataFrame(columns=["key", "query", "lat", "lon", "display", "road_km", "method"])
    cen = pd.read_csv(EXT + "district_centroids.csv"); cen["k"] = cen.dist_name.str.lower().str.replace(r"[^a-z]", "", regex=True)
    P = pd.DataFrame(test) if test is not None else load_plants()
    out = []
    for _, r in P.iterrows():
        place, dist, state = str(r.get("place", "")).strip(), str(r.get("district", "")).strip(), str(r.get("state", "")).strip()
        key = "|".join([place.lower(), dist.lower(), state.lower()])
        hit = cache[cache.key == key]
        if len(hit):
            h = hit.iloc[0]; lat, lon, disp, road, method = h.lat, h.lon, h.display, h.road_km, h.method
        else:
            g = None; method = ""
            import re as _re
            paren = _re.findall(r"\(([^)]*)\)", place); bare = _re.sub(r"\([^)]*\)", "", place).strip(" ,")
            parts = [p_.strip() for p_ in _re.split(r"[,/&]", bare) if p_.strip()]
            cands = paren + [place, bare] + parts      # the bracketed town first: 'Mohanpura (Kotputli)' matched a different Mohanpura 425 km away
            qs = []
            for c_ in cands:
                for q_ in (", ".join([x for x in (c_, dist, state, "India") if x]), ", ".join([x for x in (c_, state, "India") if x])):
                    if q_ not in qs: qs.append(q_)
            qs.append(", ".join([x for x in (dist, state, "India") if x]))
            for q in qs:
                try: g = geocode(q)
                except Exception as e: g = None
                if g: method = "nominatim: " + q; break
            lat, lon, disp = (g if g else (np.nan, np.nan, ""))
            # check against the district centroid
            dk = dist.lower().replace(" district", "")
            dk = "".join(ch for ch in dk if ch.isalpha())
            c = cen[cen.k == dk]
            # amended 23 Nov 2026 12:20 UTC, before the test was run: the 60 km rule misplaced Kotputli (110 km from the
            # Jaipur district centroid). The geocode is kept if its address is in the stated state and within 150 km of the
            # district centroid; otherwise the centroid is used and the plant flagged.
            in_state = (not state) or (state.lower().split()[0] in str(disp).lower())
            if pd.notna(lat) and ((len(c) and hav((lat, lon), (c.lat.iloc[0], c.lon.iloc[0])) > 150) or not in_state) and len(c):
                lat, lon, method = c.lat.iloc[0], c.lon.iloc[0], method + " | geocode outside the state or >150 km from the district centroid: centroid used (flag)"
            elif not len(c) and pd.isna(lat):
                method = "not geocoded"
            if pd.isna(lat) and len(c):
                lat, lon, method = c.lat.iloc[0], c.lon.iloc[0], "district centroid (geocode failed; flag)"
            try: road = route(lat, lon) if pd.notna(lat) else np.nan
            except Exception: road = np.nan
            cache = pd.concat([cache, pd.DataFrame([dict(key=key, query=f"{place}, {dist}, {state}", lat=lat, lon=lon, display=disp, road_km=road, method=method)])], ignore_index=True)
            cache.to_csv(CACHE, index=False)
        out.append({**r.to_dict(), "lat": lat, "lon": lon, "geocode": method, "geocode_display": disp, "road_km": road,
                    "straight_km": hav(DELHI, (lat, lon)) if pd.notna(lat) else np.nan})
    O = pd.DataFrame(out)
    if test is None: O.to_csv(DEL + "cement_plants_geo.csv", index=False)
    return O
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        T = main(test=[dict(place="Kotputli", district="Jaipur", state="Rajasthan"), dict(place="Dadri", district="Gautam Buddha Nagar", state="Uttar Pradesh"),
                       dict(place="Panipat", district="Panipat", state="Haryana")])
        print(T[["place", "lat", "lon", "road_km", "straight_km", "geocode"]].round(1).to_string(index=False))
    else:
        O = main(); print(len(O), "plants;", O.road_km.notna().sum(), "with road distance")
