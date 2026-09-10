# ESRI SCRIPT

import urllib.parse
import urllib.request
import json
import csv
import time
import requests
import io

import itertools

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
        "outFields": "location",
        "countryCode": "AU",
        #"outSR": "4383" # GCS_WGS_1984
        #"outSR": "7844"  # GDA2020
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


def process_input_addresses(input_file="all_addresses.csv", start_line_number=1, count=20000, start_time=None, filename_suffix=None, delimiter=","):
    # Read addresses + unique IDs from CSV
    # input_rows = []
    start_index = start_line_number - 1
    end_index = start_index + count - 1

    end_line_number = end_index + 1

    output_file = f"geocoded_output_{filename_suffix}.csv" if filename_suffix else f"geocoded_output_{start_line_number}_{end_line_number}.csv"

    # for row in reader:
    #     print(row)

    with open(input_file, newline="", encoding="utf-8") as f:

        reader = csv.reader(f)
        headers = next(reader, None)
        sliced = itertools.islice(f, start_index - 1 if start_index else 0, end_index, 1)  # Skip first 14 lines

        # reader = csv.DictReader(f)
        reader = csv.DictReader(sliced, fieldnames=headers,  delimiter=delimiter)

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["unique_id",
                            "address",
                            "lat_wgs84", "lon_wgs84",
                            "lat_gda94", "lon_gda94"]
            )

            for index, row in enumerate(reader, start=start_index):
                #input_rows.append((row["unique_id"], row["address"]))
                process_row(row, writer, index+1, start_time=start_time, total=count)
                if index >= end_index:
                    break

    return output_file, end_line_number

    # total = len(input_rows)
    #
    # print(f"Loaded {total} rows from GitHub.")

# -----------------------------
# PROCESS + WRITE OUTPUT CSV
# -----------------------------
def process_row(row, writer, current_line_number, start_time, total=2000):

        (unique_id, addr) = (row["unique_id"], row["address"])
        lat, lon, status = (None, None, "None")
        lat, lon, status = geocode_arcgis(addr)
        elapsed = time.time() - start_time

        if lat is None:
            print(f"    [line_no:{current_line_number}] Error → {status}")
            writer.writerow({
                "unique_id": unique_id,
                "address": addr,
                "lat_gda94": None,
                "lon_gda94": None
            })
        else:
            lat_gda94, lon_gda94 = wgs84_to_gda94(lat, lon)
            print(f"[{current_line_number}/{total}] Processing {unique_id}: {addr} … Success (elapsed {elapsed:.1f}s),  {lat},  {lon},  {lat_gda94},  {lon_gda94}")
            writer.writerow({
                "unique_id": unique_id,
                "address": addr,
                "lat_wgs84": lat,
                "lon_wgs84": lon,
                "lat_gda94": lat_gda94,
                "lon_gda94": lon_gda94
            })

        time.sleep(0.1)   # Nominatim rate limit



if __name__ == "__main__":

    start_time = time.time()

    input_file = "all_addresses.csv"
    count = 20_000

    # first 20_000 i.e., 1 to 20_000 addresses
    #start_line_number = 1


    # second 20_000 i.e., 20_001 to 40_000 addresses
    #start_line_number = 20_001



    # this sample "addresses_34000.csv"
    input_file = "/Users/mchalla/dev/github/addressGeocoding/new_45k_addresses.csv"
    start_line_number = 10001
    count = 10


    (output_file, end_line_number) = process_input_addresses(
        input_file=input_file,
        start_line_number=start_line_number,
        count=count if count else 20_000,
        start_time=start_time,
    )

    # Compute total time AFTER loop finishes
    total_time = time.time() - start_time

    print(f"Done. Results saved to {output_file} (rows {start_line_number}-{end_line_number})")
    print(f"Total time taken: {total_time:.1f} seconds")
