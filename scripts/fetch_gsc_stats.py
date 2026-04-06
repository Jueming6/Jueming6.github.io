#!/usr/bin/env python3
"""
Fetch Google Search Console data and update _data/gsc_stats.json.
Requires env var: GSC_SERVICE_ACCOUNT_KEY (JSON string of service account credentials)
"""

import json
import os
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

SITE_URL  = "https://jueming6.github.io/"
DATA_FILE = "_data/gsc_stats.json"

# ISO 3166-1 alpha-3 codes -> (display name, lat, lng)
COUNTRY_DATA = {
    "usa": ("United States",  37.09,  -95.71),
    "esp": ("Spain",          40.46,   -3.75),
    "ind": ("India",          20.59,   78.96),
    "ita": ("Italy",          41.87,   12.57),
    "hkg": ("Hong Kong",      22.32,  114.17),
    "aus": ("Australia",     -25.27,  133.78),
    "jpn": ("Japan",          36.20,  138.25),
    "can": ("Canada",         56.13, -106.35),
    "gbr": ("United Kingdom", 55.38,   -3.44),
    "deu": ("Germany",        51.17,   10.45),
    "fra": ("France",         46.23,    2.21),
    "kor": ("South Korea",    35.91,  127.77),
    "chn": ("China",          35.86,  104.20),
    "bra": ("Brazil",        -14.24,  -51.93),
    "sgp": ("Singapore",       1.35,  103.82),
    "nld": ("Netherlands",    52.13,    5.29),
    "swe": ("Sweden",         60.13,   18.64),
    "che": ("Switzerland",    46.82,    8.23),
    "fin": ("Finland",        61.92,   25.75),
    "nzl": ("New Zealand",   -40.90,  174.89),
    "tha": ("Thailand",       15.87,  100.99),
    "mys": ("Malaysia",        4.21,  101.98),
    "idn": ("Indonesia",      -0.79,  113.92),
    "phl": ("Philippines",    12.88,  121.77),
    "vnm": ("Vietnam",        14.06,  108.28),
    "bgd": ("Bangladesh",     23.68,   90.36),
    "twn": ("Taiwan",         23.70,  121.00),
    "per": ("Peru",            -9.19,  -75.02),
    "sau": ("Saudi Arabia",   23.89,   45.08),
    "dza": ("Algeria",        28.03,    1.66),
    "lbn": ("Lebanon",        33.85,   35.86),
    "sdn": ("Sudan",          12.86,   30.22),
    "bol": ("Bolivia",       -16.29,  -63.59),
    "cri": ("Costa Rica",      9.75,  -83.75),
    "est": ("Estonia",        58.60,   25.01),
    "som": ("Somalia",         5.15,   46.20),
    "cze": ("Czechia",        49.82,   15.47),
    "pri": ("Puerto Rico",    18.22,  -66.59),
    "mac": ("Macau",          22.16,  113.55),
    "mex": ("Mexico",         23.63,  -102.55),
    "arg": ("Argentina",     -38.42,  -63.62),
    "zaf": ("South Africa",  -30.56,   22.94),
    "egy": ("Egypt",          26.82,   30.80),
    "tur": ("Turkey",         38.96,   35.24),
    "pak": ("Pakistan",       30.38,   69.35),
    "irn": ("Iran",           32.43,   53.69),
    "irq": ("Iraq",           33.22,   43.68),
    "uga": ("Uganda",         -1.37,   32.29),
    "ken": ("Kenya",          -0.02,   37.91),
    "ngr": ("Nigeria",         9.08,    8.68),
    "prt": ("Portugal",       39.40,   -8.22),
    "pol": ("Poland",         51.92,   19.15),
    "ukr": ("Ukraine",        48.38,   31.17),
    "rou": ("Romania",        45.94,   24.97),
    "grc": ("Greece",         39.07,   21.82),
    "dnk": ("Denmark",        56.26,    9.50),
    "nor": ("Norway",         60.47,    8.47),
    "bel": ("Belgium",        50.50,    4.47),
    "aut": ("Austria",        47.52,   14.55),
    "hun": ("Hungary",        47.16,   19.50),
    "isr": ("Israel",         31.05,   34.85),
    "are": ("UAE",            23.42,   53.85),
    "mya": ("Myanmar",        21.91,   95.96),
    "lka": ("Sri Lanka",       7.87,   80.77),
    "npl": ("Nepal",          28.39,   84.12),
    "khm": ("Cambodia",       12.57,  104.99),
}


def get_service():
    key_json = os.environ["GSC_SERVICE_ACCOUNT_KEY"]
    creds = service_account.Credentials.from_service_account_info(
        json.loads(key_json),
        scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
    )
    return build("searchconsole", "v1", credentials=creds)


def query(service, start_date, end_date, dimensions, row_limit=5000):
    resp = service.searchanalytics().query(
        siteUrl=SITE_URL,
        body={"startDate": start_date, "endDate": end_date,
              "dimensions": dimensions, "rowLimit": row_limit}
    ).execute()
    return resp.get("rows", [])


def main():
    svc = get_service()

    end_date   = datetime.today().strftime("%Y-%m-%d")
    # GSC keeps ~16 months; fetch from earliest available
    start_date = (datetime.today() - timedelta(days=480)).strftime("%Y-%m-%d")

    # Daily clicks
    daily_rows = query(svc, start_date, end_date, ["date"])
    daily = sorted(
        [{"date": r["keys"][0], "clicks": int(r["clicks"])} for r in daily_rows],
        key=lambda x: x["date"]
    )

    # Country clicks
    country_rows = query(svc, start_date, end_date, ["country"])
    countries = []
    for r in country_rows:
        if int(r["clicks"]) > 0:
            code = r["keys"][0].lower()
            if code in COUNTRY_DATA:
                name, lat, lng = COUNTRY_DATA[code]
                countries.append({"name": name, "lat": lat, "lng": lng, "clicks": int(r["clicks"])})
    countries.sort(key=lambda x: -x["clicks"])

    total_clicks = sum(c["clicks"] for c in countries)

    stats = {
        "total_clicks":    total_clicks,
        "total_countries": len(countries),
        "updated":         end_date,
        "countries":       countries,
        "daily":           daily
    }

    with open(DATA_FILE, "w") as f:
        json.dump(stats, f, indent=2)

    print(f"Done: {total_clicks} clicks, {len(countries)} countries, {len(daily)} daily rows -> {DATA_FILE}")


if __name__ == "__main__":
    main()
