#!/usr/bin/env python3
"""
Fetch GoatCounter stats and update _data/gsc_stats.json.
Env vars: GOATCOUNTER_CODE (e.g. "jueming"), GOATCOUNTER_TOKEN (API token).
"""

import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

DATA_FILE = "_data/gsc_stats.json"
BASELINE_FILE = "_data/gsc_baseline.json"

# ISO 3166-1 alpha-2 -> (display name, lat, lng)
COUNTRY_DATA = {
    "US": ("United States", 37.09, -95.71),
    "ES": ("Spain", 40.46, -3.75),
    "IN": ("India", 20.59, 78.96),
    "IT": ("Italy", 41.87, 12.57),
    "HK": ("Hong Kong", 22.32, 114.17),
    "AU": ("Australia", -25.27, 133.78),
    "JP": ("Japan", 36.20, 138.25),
    "CA": ("Canada", 56.13, -106.35),
    "GB": ("United Kingdom", 55.38, -3.44),
    "DE": ("Germany", 51.17, 10.45),
    "FR": ("France", 46.23, 2.21),
    "KR": ("South Korea", 35.91, 127.77),
    "CN": ("China", 35.86, 104.20),
    "BR": ("Brazil", -14.24, -51.93),
    "SG": ("Singapore", 1.35, 103.82),
    "NL": ("Netherlands", 52.13, 5.29),
    "SE": ("Sweden", 60.13, 18.64),
    "CH": ("Switzerland", 46.82, 8.23),
    "FI": ("Finland", 61.92, 25.75),
    "NZ": ("New Zealand", -40.90, 174.89),
    "TH": ("Thailand", 15.87, 100.99),
    "MY": ("Malaysia", 4.21, 101.98),
    "ID": ("Indonesia", -0.79, 113.92),
    "PH": ("Philippines", 12.88, 121.77),
    "VN": ("Vietnam", 14.06, 108.28),
    "BD": ("Bangladesh", 23.68, 90.36),
    "TW": ("Taiwan", 23.70, 121.00),
    "PE": ("Peru", -9.19, -75.02),
    "SA": ("Saudi Arabia", 23.89, 45.08),
    "DZ": ("Algeria", 28.03, 1.66),
    "LB": ("Lebanon", 33.85, 35.86),
    "SD": ("Sudan", 12.86, 30.22),
    "BO": ("Bolivia", -16.29, -63.59),
    "CR": ("Costa Rica", 9.75, -83.75),
    "EE": ("Estonia", 58.60, 25.01),
    "SO": ("Somalia", 5.15, 46.20),
    "CZ": ("Czechia", 49.82, 15.47),
    "PR": ("Puerto Rico", 18.22, -66.59),
    "MO": ("Macau", 22.16, 113.55),
    "MX": ("Mexico", 23.63, -102.55),
    "AR": ("Argentina", -38.42, -63.62),
    "ZA": ("South Africa", -30.56, 22.94),
    "EG": ("Egypt", 26.82, 30.80),
    "TR": ("Turkey", 38.96, 35.24),
    "PK": ("Pakistan", 30.38, 69.35),
    "IR": ("Iran", 32.43, 53.69),
    "IQ": ("Iraq", 33.22, 43.68),
    "UG": ("Uganda", -1.37, 32.29),
    "KE": ("Kenya", -0.02, 37.91),
    "NG": ("Nigeria", 9.08, 8.68),
    "PT": ("Portugal", 39.40, -8.22),
    "PL": ("Poland", 51.92, 19.15),
    "UA": ("Ukraine", 48.38, 31.17),
    "RO": ("Romania", 45.94, 24.97),
    "GR": ("Greece", 39.07, 21.82),
    "DK": ("Denmark", 56.26, 9.50),
    "NO": ("Norway", 60.47, 8.47),
    "BE": ("Belgium", 50.50, 4.47),
    "AT": ("Austria", 47.52, 14.55),
    "HU": ("Hungary", 47.16, 19.50),
    "IL": ("Israel", 31.05, 34.85),
    "AE": ("UAE", 23.42, 53.85),
    "MM": ("Myanmar", 21.91, 95.96),
    "LK": ("Sri Lanka", 7.87, 80.77),
    "NP": ("Nepal", 28.39, 84.12),
    "KH": ("Cambodia", 12.57, 104.99),
    "RU": ("Russia", 61.52, 105.32),
    "CL": ("Chile", -35.68, -71.54),
    "CO": ("Colombia", 4.57, -74.30),
    "VE": ("Venezuela", 6.42, -66.59),
    "EC": ("Ecuador", -1.83, -78.18),
    "IE": ("Ireland", 53.41, -8.24),
    "SK": ("Slovakia", 48.67, 19.70),
    "SI": ("Slovenia", 46.15, 14.99),
    "HR": ("Croatia", 45.10, 15.20),
    "BG": ("Bulgaria", 42.73, 25.49),
    "LT": ("Lithuania", 55.17, 23.88),
    "LV": ("Latvia", 56.88, 24.60),
    "LU": ("Luxembourg", 49.82, 6.13),
    "IS": ("Iceland", 64.96, -19.02),
    "MA": ("Morocco", 31.79, -7.09),
    "TN": ("Tunisia", 33.89, 9.54),
    "ET": ("Ethiopia", 9.15, 40.49),
    "TZ": ("Tanzania", -6.37, 34.89),
    "GH": ("Ghana", 7.95, -1.02),
    "JO": ("Jordan", 30.59, 36.24),
    "QA": ("Qatar", 25.35, 51.18),
    "KW": ("Kuwait", 29.31, 47.48),
    "OM": ("Oman", 21.51, 55.92),
    "BH": ("Bahrain", 25.93, 50.64),
}


def api_get(path, code, token):
    url = f"https://{code}.goatcounter.com/api/v0{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        raise SystemExit(f"HTTP {e.code} from {url}\nResponse body: {body}")


def main():
    code = os.environ["GOATCOUNTER_CODE"].strip()
    token = os.environ["GOATCOUNTER_TOKEN"].strip()
    print(f"Using subdomain: {code}.goatcounter.com")

    # Health check — validates subdomain + token before the real query
    api_get("/me", code, token)

    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=365 * 2)
    params = f"?start={start.isoformat()}&end={end.isoformat()}&limit=200"

    # Start from the frozen GSC baseline (pre-GoatCounter history)
    merged = {}  # code -> {name, lat, lng, clicks}
    try:
        with open(BASELINE_FILE) as f:
            baseline = json.load(f)
        for c in baseline.get("countries", []):
            merged[c["code"].upper()] = {
                "name": c["name"], "lat": c["lat"], "lng": c["lng"],
                "clicks": int(c.get("clicks", 0)),
            }
    except FileNotFoundError:
        pass

    # Add GoatCounter counts on top
    loc = api_get(f"/stats/locations{params}", code, token)
    print(f"GoatCounter /stats/locations raw response: {json.dumps(loc)[:800]}")
    try:
        total = api_get(f"/stats/total{params}", code, token)
        print(f"GoatCounter /stats/total: {json.dumps(total)[:400]}")
    except SystemExit as e:
        print(f"(total probe failed: {e})")
    for row in loc.get("stats", []):
        cid = (row.get("id") or "").upper()
        count = int(row.get("count", 0))
        if count <= 0 or not cid:
            continue
        if cid in merged:
            merged[cid]["clicks"] += count
        elif cid in COUNTRY_DATA:
            name, lat, lng = COUNTRY_DATA[cid]
            merged[cid] = {"name": name, "lat": lat, "lng": lng, "clicks": count}
        else:
            merged[cid] = {"name": row.get("name") or cid, "lat": 0.0, "lng": 0.0, "clicks": count}

    countries = sorted(merged.values(), key=lambda x: -x["clicks"])

    total_clicks = sum(c["clicks"] for c in countries)

    stats = {
        "total_clicks": total_clicks,
        "total_countries": len(countries),
        "updated": end.isoformat(),
        "countries": countries,
    }

    with open(DATA_FILE, "w") as f:
        json.dump(stats, f, indent=2)

    print(f"Done: {total_clicks} visits, {len(countries)} countries -> {DATA_FILE}")


if __name__ == "__main__":
    main()
