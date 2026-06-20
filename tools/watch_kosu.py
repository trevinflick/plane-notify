"""
Standalone helper, not wired into the main bot. Polls airplanes.live's free
public API for traffic near a given airport and logs business-jet-sized
contacts to a CSV, flagging Bombardier Global hits. Useful for catching a
tail number live or re-confirming a sighting, without needing any API key.

Usage: pipenv run python tools/watch_kosu.py
"""
import csv
import os
import sys
import time
from datetime import datetime, timezone

import requests

KOSU = (40.0807, -83.0735)
RADIUS_NM = 50
POLL_SECONDS = 60
LARGE_JET_CATEGORIES = {"A2", "A3", "A5"}
BOMBARDIER_GLOBAL_TYPES = {"GL5T", "GL6T", "GLEX", "GL7T", "GLF6"}
LOG_PATH = os.path.join(os.path.dirname(__file__), "watch_kosu_sightings.csv")

def poll(lat, lon, radius_nm):
    url = f"https://api.airplanes.live/v2/point/{lat}/{lon}/{radius_nm}"
    headers = {"User-Agent": "plane-notify (https://github.com/Jxck-S/plane-notify)"}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json().get("ac", [])

def log_sighting(writer, ac, flagged):
    writer.writerow([
        datetime.now(timezone.utc).isoformat(),
        ac.get("hex"), ac.get("r"), ac.get("t"), ac.get("desc"), ac.get("ownOp"),
        ac.get("lat"), ac.get("lon"), ac.get("alt_baro"), ac.get("gs"),
        "BOMBARDIER GLOBAL" if flagged else "",
    ])

def main():
    is_new_file = not os.path.isfile(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new_file:
            writer.writerow(["seen_at_utc", "hex", "reg", "type", "desc", "ownOp",
                              "lat", "lon", "alt_baro", "gs", "flag"])
        while True:
            try:
                aircraft = poll(*KOSU, RADIUS_NM)
            except Exception as e:
                print(f"Error polling airplanes.live: {e}")
                aircraft = []
            for ac in aircraft:
                flagged = ac.get("t") in BOMBARDIER_GLOBAL_TYPES
                if flagged or ac.get("category") in LARGE_JET_CATEGORIES:
                    log_sighting(writer, ac, flagged)
                    f.flush()
                    marker = "  <-- BOMBARDIER GLOBAL" if flagged else ""
                    print(f"{ac.get('r', '?'):8s} {ac.get('t', '?'):6s} {ac.get('desc', ''):40s}{marker}")
            sys.stdout.write(f"\rPolled {len(aircraft)} contacts within {RADIUS_NM}nm of KOSU, sleeping {POLL_SECONDS}s...")
            sys.stdout.flush()
            time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
