# ESRI SCRIPT

import urllib.parse
import urllib.request
import json
import csv
import time
import requests
import io

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "GitHubGeocoderDemo/1.0"}


# -----------------------------
# WGS84 → GDA94 conversion
# -----------------------------
def wgs84_to_gda94(lat, lon):
    # Approximate Australia-wide shift
    lat_gda94 = lat + 0.0000005
    lon_gda94 = lon + 0.0000011
    return lat_gda94, lon_gda94


# -----------------------------
# Geocode using Nominatim
# -----------------------------
def geocode_address(address):
    params = urllib.parse.urlencode(
        {
            "q": address,
            "format": "json",
            "limit": 1
        }
    )
    url = NOMINATIM_URL + "?" + params

    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        # ALWAYS return 3 values
        return None, None, f"Error: {e}"

    if not data:
        return None, None, "No results found"

    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon, "OK"



# -----------------------------
# Geocode using ARCGIS
# -----------------------------
def geocode_arcgis(address):
    url = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"

    params = {
        "f": "json",
        "singleLine": address,
        "outFields": "*"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    candidates = data.get("candidates", [])
    if not candidates:
        return None, None, "None"


    # ArcGIS returns x = longitude, y = latitude
    loc = candidates[0]["location"]
    lon = loc["x"]
    lat = loc["y"]
    
    return lat, lon, "OK"

# Read addresses + unique IDs from CSV
input_rows = []
with open("addresses_34000.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        input_rows.append((row["unique_id"], row["address"]))

total = len(input_rows)


total = len(input_rows)
print(f"Loaded {total} rows from GitHub.")


# -----------------------------
# PROCESS + WRITE OUTPUT CSV
# -----------------------------
start_time = time.time()  # total timer start

# Write results to output CSV
with open("geocoded_output_34000.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["unique_id",
                    "address",
                    "lat_wgs84", "lon_wgs84",
                    "lat_gda94", "lon_gda94"]
    )
    writer.writeheader()

    for index, (unique_id, addr) in enumerate(input_rows, start=1):
        elapsed = time.time() - start_time

        #lat, lon, status = geocode_address(addr)
        lat, lon, status = geocode_arcgis(addr)


        if lat is None:
            print(f"    Error → {status}")
            writer.writerow({
                "unique_id": unique_id,
                "address": addr,
                "lat_gda94": None,
                "lon_gda94": None
            })
        else:
            lat_gda94, lon_gda94 = wgs84_to_gda94(lat, lon)
            print(f"[{index}/{total}] Processing {unique_id}: {addr} … Success (elapsed {elapsed:.1f}s),  {lat},  {lon},  {lat_gda94},  {lon_gda94}")
            writer.writerow({
                "unique_id": unique_id,
                "address": addr,
                "lat_wgs84": lat,
                "lon_wgs84": lon,
                "lat_gda94": lat_gda94,
                "lon_gda94": lon_gda94
            })

        time.sleep(1)   # Nominatim rate limit

# Compute total time AFTER loop finishes
total_time = time.time() - start_time

print("Done. Results saved to geocoded_output_34000.csv")
print(f"Total time taken: {total_time:.1f} seconds")
