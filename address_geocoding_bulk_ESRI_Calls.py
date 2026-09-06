import csv
import json
import requests
import time

INPUT_FILE = "addresses.csv"
OUTPUT_FILE = "geocoded_output.csv"
BATCH_SIZE = 10

ARC_URL = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"
# ARC_URL ="https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/geocodeAddresses"

def geocode_batch(batch_records):
    """
    batch_records = list of tuples: (unique_id, address)
    Sends up to 10 addresses in one ArcGIS batch request.
    """

    payload = {
        "f": "json",
        "maxLocations": 1,
        "addresses": json.dumps({
            "records": [
                {
                    "attributes": {
                        "objectid": unique_id,
                        "SingleLine": address
                    }
                }
                for i, (unique_id, address) in enumerate(batch_records)
            ]
        })
    }

    response = requests.post(ARC_URL, data=payload)
    response.raise_for_status()
    return response.json()


# Read input CSV
with open(INPUT_FILE, newline="", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    rows = [(row["unique_id"], row["address"]) for row in reader]


# Write output CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=["unique_id", "address", "lat", "lon"])
    writer.writeheader()

    # Process in batches of 10
    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        print(f"Processing batch {i//BATCH_SIZE + 1} with {len(batch)} addresses")

        result = geocode_batch(batch)

        # Fixed: Changed result.len to len(result.get("locations", []))
        print(f"Number of locations in result: {len(result.get("locations", []))}")

        # ArcGIS returns results in "locations"
        for rec in result.get("locations", []):
            objid = rec["attributes"]["ResultID"]
            unique_id, address = batch[objid]

            loc = rec["location"]
            lat, lon = loc["y"], loc["x"]

            writer.writerow({
                "unique_id": unique_id,
                "address": address,
                "lat": lat,
                "lon": lon
            })

            print(f"{unique_id} | {address} → {lat}, {lon}")

        time.sleep(0.3)  # polite pacing
