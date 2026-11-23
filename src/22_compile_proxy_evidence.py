"""Compile the Step 1b evidence into one table in the layout of manual_collection/proxy_evidence_template.csv.

One row per plant and proxy (night lights, radar flood water) for the zone plants of firms with at
least 5% of plant cost in the zone, plus the third-party rows that name a sample firm.
Output: research/proxy_evidence.csv
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
NAME = {"E_CHE_FLOOD_2023": "chennai_2023", "E_GJ_FLOOD_2024": "gujarat_2024", "E_GJ_FLOOD_2023": "gujarat_2023"}
ntl = pd.read_csv(TAB + "ntl_plant_event.csv"); fi = pd.read_csv(TAB + "ntl_firm_event.csv")
keep = fi[fi.share_zone >= 0.05][["event_id", "nse_symbol"]]
rows = []
for r in ntl.merge(keep, on=["event_id", "nse_symbol"]).itertuples():
    if not r.lit: note, val = "site not lit at night in normal times (baseline < 5 nW/cm2/sr) or coordinate outside the zone: no reading possible", ""
    elif not r.observed: note, val = "cloud: no clean night in the first week after the event", ""
    else:
        val = round(r.ratio_first, 2)
        note = ("DARK: below 60% of the site's normal on the first clean night" if r.dark is True or r.dark == True  # noqa: E712
                else "not dark on the first clean night") + f"; plant cost share of firm {0 if pd.isna(r.plant_share) else r.plant_share:.3f}; industry {r.industry}"
    rows.append(dict(event=NAME[r.event_id], nse_symbol=r.nse_symbol, plant_lat=round(r.lat, 5), plant_lon=round(r.lon, 5), district=r.dist_name,
                     proxy_type="night_lights_ratio_to_normal", date=r.first_clean_night if isinstance(r.first_clean_night, str) else "", value=val,
                     baseline_value=round(r.base_radiance, 1) if pd.notna(r.base_radiance) else "",
                     days_affected=r.first_night_back_above_0_8 if pd.notna(r.first_night_back_above_0_8) else "",
                     source_url="NASA Black Marble VNP46A2 v2, doi:10.5067/VIIRS/VNP46A2.002 (src/14_ntl_extract.py)", notes=note))
if os.path.exists(TAB + "flood_plant_event.csv"):
    fl = pd.read_csv(TAB + "flood_plant_event.csv")
    for r in fl.merge(keep, on=["event_id", "nse_symbol"]).itertuples():
        if not r.coord_ok: continue
        if not r.observed_event: note, val = "no Sentinel-1 radar pass over the plant in the event window", ""
        else:
            val = int(r.flood_px_500_event)
            note = (f"flood pixels (20 m) within 500 m; within 1 km: {int(r.flood_px_1000_event)}; nearest flood water "
                    + (f"{r.nearest_flood_m_event:.0f} m" if pd.notna(r.nearest_flood_m_event) else "more than 1 km away")
                    + f"; radar blind over {100 * r.excluded_frac_500:.0f}% of the 500 m circle")
        rows.append(dict(event=NAME[r.event_id], nse_symbol=r.nse_symbol, plant_lat=round(r.lat, 5), plant_lon=round(r.lon, 5), district=r.dist_name,
                         proxy_type="radar_flood_pixels_within_500m", date=r.event_pass_dates if isinstance(r.event_pass_dates, str) else "", value=val,
                         baseline_value=r.flood_px_500_before if pd.notna(r.flood_px_500_before) else "", days_affected="",
                         source_url="Copernicus Global Flood Monitoring, https://stac.eodc.eu/api/v1/collections/GFM (src/16_flood_gfm.py)", notes=note))
if os.path.exists(TAB + "nrsc_chennai_plants.csv"):            # Round 4: NRSC RISAT-1A flood map of 7 Dec 2023 (33_nrsc_chennai_flood.py)
    nr = pd.read_csv(TAB + "nrsc_chennai_plants.csv")
    keep_che = keep[keep.event_id == "E_CHE_FLOOD_2023"].nse_symbol
    for r in nr[nr.nse_symbol.isin(keep_che)].itertuples():
        rows.append(dict(event="chennai_2023", nse_symbol=r.nse_symbol, plant_lat=round(r.lat, 5), plant_lon=round(r.lon, 5), district=r.dist_name,
                         proxy_type="nrsc_radar_flood_share_500m", date="2023-12-07", value=round(r.flood_frac_500, 4), baseline_value="", days_affected="",
                         source_url="NRSC/ISRO map 2023/CY/TN/01a/07122023 (RISAT-1A, 7 Dec 2023), via NDEM; research/proxy/docs/NDEM_TN_Michaung_7Dec2023_map.pdf",
                         notes=("nearest flood/standing-water pixel " + (f"{r.nearest_flood_m:.0f} m" if pd.notna(r.nearest_flood_m) else "more than ~2 km away")
                                + "; radar cannot see water between buildings; map includes standing water in paddy fields")))
for f in ("third_party_chennai_2023.csv", "third_party_gujarat.csv"):
    p = ROOT + "/research/proxy/" + f
    if not os.path.exists(p): continue
    t = pd.read_csv(p, dtype=str).fillna("")
    for r in t[t.nse_symbol != ""].itertuples():
        rows.append(dict(event=r.event, nse_symbol=r.nse_symbol, plant_lat="", plant_lon="", district=r.location, proxy_type="third_party_" + r.topic,
                         date=r.date_of_fact, value=r.value, baseline_value="", days_affected=r.days_affected, source_url=r.source_url,
                         notes=f"{r.finding} | quote: {r.source_quote} | read: {r.read_mode}"))
o = pd.DataFrame(rows); o.to_csv(ROOT + "/research/proxy_evidence.csv", index=False)
print(len(o), "rows;", o.groupby(["event", "proxy_type"]).size().to_string())
