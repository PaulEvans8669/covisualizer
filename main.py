import requests
import time
import json
import os
from Models.Country import Country

places_file = "places.json"


def getLatLon(init_location):
    location = init_location.replace(" ", "%20")

    if "diamond" in location or "recovered" in location:
        pass

    location = location.replace(" ", "%20")\
        .replace("(", "")\
        .replace(")", "")\
        .replace("'", "")\
        .replace("*", "")
    query = \
        "https://eu1.locationiq.com/v1/search.php?key=bc4980331944cc&q=" \
        + location + "&format=json&limit=1"
    resp = requests.get(query)
    data = resp.json()

    try:
        lat = data[0]['lat']
        lon = data[0]['lon']
        print(init_location + " : " + lat + " " + lon)
        return lat, lon
    except KeyError:
        print("ERROR")
        print(data)


def UpdateLocation(fileData, json_data):
    banned_words = {"diamond princess", "recovered"}
    already_saved = set(fileData)
    new_locs = set()
    for e in json_data:

        if e['province'] is not None:
            to_add = e['province'] + " " + e['country']
        else:
            to_add = e['country']

        if not any([substr in to_add for substr in banned_words]):
            new_locs.add(to_add)

    diff = new_locs - already_saved
    print("LOCATIONS UPDATES ================= ")
    print("Locations to update : " + str(len(diff)))

    # print(diff)
    for e in diff:
        loc = dict()
        lat, lon = getLatLon(e)
        loc["lat"] = lat
        loc["lon"] = lon
        fileData[e] = loc
        time.sleep(1)
    # print(fileData)


def Update(json_data):
    file_data = {}
    if os.stat(places_file).st_size != 0:
        # if file is not  empty
        try:
            places_jsonFile = open(places_file, "r")
            file_data = json.load(places_jsonFile)
            places_jsonFile.close()
        except FileNotFoundError:
            print("File places.json does not exist... Creating it.")

    places_jsonFile = open(places_file, "w")

    if len(file_data) != len(json_data):
        UpdateLocation(file_data, json_data)
        new_data = json.dumps(file_data)
        places_jsonFile.write(new_data)
    places_jsonFile.close()


banned_words = {"diamond princess", "recovered"}

response = requests.get("https://corona.lmao.ninja/v2/historical")

countries = []
if response.status_code == 200:
    website_data = response.json()
    Update(website_data)
    print("Location updates done =============")
    for i in range(len(website_data)):
        if website_data[i]['province'] is not None:
            to_add = website_data[i]['province'] \
                     + " " + website_data[i]['country']
        else:
            to_add = website_data[i]['country']
        if not any([substr in to_add for substr in banned_words]):
            countries.append(Country(website_data[i]))
else:
    print("API ERROR")

jsonFile = open(places_file, "r")
data = json.load(jsonFile)
for c in countries:
    key = ""
    if c.province:
        key += c.province + " "
    key += c.name
    pos = data[key]
    c.lat = float(pos['lat'])
    c.lon = float(pos['lon'])

dates = countries[0].cases.keys()

print("GENERATING DATA FILE ==============")
print("Total locations : " + str(len(countries)))
print("Total days of data : " + str(len(dates)))
globe_data = []
for type in ['c', 'd']:
    for date in dates:
        series = [date + "_" + type]
        s_data = []
        add = False
        for c in countries:
            s_data.append(round(c.lat))
            s_data.append(round(c.lon))
            if type == 'c':
                val = round(c.cases[date] / Country.maxCases, 3)
            else:
                val = round(c.deaths[date] / Country.maxDeaths, 3)
            s_data.append(val)
        series.append(s_data)
        globe_data.append(series)

json_globe_data = json.dumps(globe_data)
json_globe_data = json_globe_data.replace("-0.0,", "0.000,")
json_globe_data = json_globe_data.replace("0.0,", "0.000,")

data_file = "data.json"
jsonFile = open(data_file, "w")
jsonFile.write(json_globe_data)
jsonFile.close()

print("Done generating data file =========")
