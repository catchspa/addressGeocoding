import csv
import json
import requests
import time

INPUT_FILE = "addresses.csv"
OUTPUT_FILE = "geocoded_output.csv"
BATCH_SIZE = 5

ARC_URL = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"

def geocode_batch(address_list):
    """
    Send up to 5 addresses in one request using ArcGIS 'addresses' parameter.
    """
    payload = {
        "f": "json",
        "addresses": json.dumps({
            "records": [
                {"attributes": {"OBJECTID": i, "SingleLine": addr}}
                for i, addr in enumerate(address_list)
            ]
        }),
        "maxLocations": 1
    }

    response = requests.post(ARC_URL, data=payload)
    response.raise_for_status()
    return response.json()

# Read input CSV
with open(INPUT_FILE, newline="", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    rows = [(row["unique_id"], row["address"]) for row in reader]

# Prepare output CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=["address", "lat", "lon"])
    writer.writeheader()

    # Process in batches of 5
    for i in range(0, len(addresses), BATCH_SIZE):
        batch = addresses[i:i + BATCH_SIZE]
        print(f"Processing batch {i//BATCH_SIZE + 1} with {len(batch)} addresses")

        result = geocode_batch(batch)

        # Parse results
        for rec in result.get("locations", []):
            objid = rec["attributes"]["ResultID"]
            addr = batch[objid]
            loc = rec["location"]
            lat, lon = loc["y"], loc["x"]

            writer.writerow({"address": addr, "lat": lat, "lon": lon})
            print(f"{addr} → {lat}, {lon}")

        time.sleep(0.3)  # polite pacing
