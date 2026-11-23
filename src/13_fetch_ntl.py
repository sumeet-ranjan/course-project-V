"""Download NASA Black Marble daily night-time lights (VNP46A2, collection 2) for the event windows.

Source: NASA LAADS DAAC cloud archive (data.laadsdaac.earthdatacloud.nasa.gov), found through the
public CMR granule search. Needs a free NASA Earthdata login:
  * in the cloud session it is a network secret saved for host urs.earthdata.nasa.gov (the proxy
    adds it; this script never sees it);
  * anywhere else put `machine urs.earthdata.nasa.gov login <user> password <pw>` in ~/.netrc.
Raw tiles (~19 MB each) go to external/ntl_raw/ (excluded from the zip). 14_ntl_extract.py turns
them into the small per-plant table that is kept.

Tiles: 10 x 10 degree, 15 arc-second grid. h = floor((lon+180)/10), v = floor((90-lat)/10).
  Chennai zone (lon 79.7-80.35, lat 12.3-13.4) straddles h25v07 and h26v07.
  Gujarat zone (lon 72.1-74.8, lat 20.6-22.9) is h25v06.
Date convention (checked against VNP46A1 UTC_Time, see README 5.7): the file for UTC day D is the
overpass at about 20:00 UTC on day D = about 01:30 IST on day D+1.
"""
import os, sys, json, subprocess, urllib.request, urllib.parse, datetime as dt
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = ROOT + "/external/ntl_raw/"
os.makedirs(RAW, exist_ok=True)

# event -> (first rain / flood date used in common.EVENTS, tiles)
WINDOWS = {
    "E_CHE_FLOOD_2023": ("2023-12-04", ["h25v07", "h26v07"]),
    "E_GJ_FLOOD_2024":  ("2024-08-25", ["h25v06"]),
    "E_GJ_FLOOD_2023":  ("2023-09-16", ["h25v06"]),
}
PRE, POST = 31, 30
PRODUCT = sys.argv[1] if len(sys.argv) > 1 else "VNP46A2"

def cmr(tile, d0, d1):
    q = {"short_name": PRODUCT, "temporal": f"{d0}T00:00:00Z,{d1}T23:59:59Z", "page_size": "200",
         "readable_granule_name": f"*{tile}*", "options[readable_granule_name][pattern]": "true"}
    u = "https://cmr.earthdata.nasa.gov/search/granules.json?" + urllib.parse.urlencode(q)
    d = json.load(urllib.request.urlopen(u, timeout=120))
    out = []
    for e in d["feed"]["entry"]:
        for l in e["links"]:
            if l["href"].startswith("https://data.laadsdaac") and l["href"].endswith(".h5"):
                out.append(l["href"])
    return sorted(set(out))

def fetch(args):
    i, url = args
    fn = RAW + os.path.basename(url)
    if os.path.exists(fn) and os.path.getsize(fn) > 1_000_000:
        return fn, "cached"
    jar = RAW + f".cookies_{i % 4}.txt"
    for attempt in range(4):
        r = subprocess.run(["curl", "-sS", "-L", "--netrc-optional", "-m", "600", "-c", jar, "-b", jar,
                            "-o", fn + ".part", "-w", "%{http_code}", url], capture_output=True, text=True)
        ok = r.stdout.strip() == "200" and os.path.exists(fn + ".part")
        if ok:
            with open(fn + ".part", "rb") as f:
                ok = f.read(8) == b"\x89HDF\r\n\x1a\n"
        if ok:
            os.replace(fn + ".part", fn)
            return fn, "ok"
        subprocess.run(["sleep", str(5 * (attempt + 1))])
    return fn, f"FAILED http={r.stdout.strip()} {r.stderr.strip()[:120]}"

if __name__ == "__main__":
    urls = []
    for ev, (start, tiles) in WINDOWS.items():
        s = dt.date.fromisoformat(start)
        d0, d1 = s - dt.timedelta(days=PRE), s + dt.timedelta(days=POST)
        for t in tiles:
            u = cmr(t, d0, d1)
            print(ev, t, d0, d1, len(u), "granules listed (of", (d1 - d0).days + 1, "days)", flush=True)
            urls += u
    urls = sorted(set(urls))
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(fetch, enumerate(urls)))
    bad = [r for r in res if r[1].startswith("FAILED")]
    print(len(res), "files;", sum(r[1] == "ok" for r in res), "downloaded,",
          sum(r[1] == "cached" for r in res), "cached,", len(bad), "failed")
    for b in bad: print("  ", b)
