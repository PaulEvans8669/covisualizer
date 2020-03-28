import requests
import time
import json
from Models.Country import Country

update_file = "places.json"

def getLatLon(location):
    location = location.replace(" ","%20")

    if "diamond" in location or "recovered" in location:
        pass

    try:
        location = location.replace(" ", "%20")
        location = location.replace("(", "")
        location = location.replace(")", "")
        location = location.replace("'", "")
        location = location.replace("*", "")
        query = "https://eu1.locationiq.com/v1/search.php?key=bc4980331944cc&q="+location+"&format=json&limit=1"
        resp = requests.get(query)
        data = resp.json()
        lat = data[0]['lat']
        lon = data[0]['lon']
        print(location + " : " + lat + " " + lon)
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
        else:
            print("banned word match : " + to_add +". Removing element from locations list.")
    diff = new_locs - already_saved
    print("Locaitons to update : " + str(len(diff)) + " 1 per second (API limit)")
    print(diff)
    for e in diff:
        loc = dict()
        lat, lon = getLatLon(e)
        loc["lat"] = lat
        loc["lon"] = lon
        fileData[e] = loc
        time.sleep(1)
    print(fileData)


def Update(json_data):
    jsonFile = open(update_file, "r+")
    data = json.load(jsonFile)

    if len(data) != len(json_data):
        jsonFile.seek(0)
        jsonFile.truncate()
        UpdateLocation(data, json_data)
        new_data = json.dumps(data)
        jsonFile.write(new_data)
    jsonFile.close()


banned_words = {"diamond princess", "recovered"}
test = {'ethiopia', 'uk', 'barbados', 'greenland denmark', 'cabo verde', 'france', 'mozambique', 'west bank and gaza', 'belgium', 'northwest territories canada', 'cuba', 'portugal', 'spain', 'manitoba canada', 'tianjin china', 'aruba netherlands', 'jordan', 'gibraltar uk', 'recovered canada', 'northern territory australia', 'bahamas', 'greece', 'holy see', 'serbia', 'usa', 'ghana', 'french polynesia france', 'jiangsu china', 'henan china', 'quebec canada', 'chongqing china', 'iraq', 'armenia', 'tasmania australia', 'austria', 'bangladesh', 'guyana', 'hunan china', 'hainan china', 'central african republic', 'macau china', 'mayotte france', 'algeria', 'monaco', 'new zealand', 'saudi arabia', 'ecuador', 'uganda', 'guadeloupe france', 'nova scotia canada', 'kenya', 'libya', 'tanzania', 'madagascar', 'hungary', 'congo (kinshasa)', 'thailand', 'latvia', 'iceland', 'malaysia', 'finland', 'reunion france', 'saskatchewan canada', 'yukon canada', 'nicaragua', 'sudan', 'trinidad and tobago', 'kosovo', 'french guiana france', 'south africa', 'congo (brazzaville)', "cote d'ivoire", 'turkey', 'kazakhstan', 'el salvador', 'syria', 'malta', 'guizhou china', 'belize', 'peru', 'uae', 'gansu china', 'niger', 'norway', 'qatar', 'guangxi china', 'south australia australia', 'nepal', 'italy', 'queensland australia', 'honduras', 'cayman islands uk', 'uzbekistan', 'bermuda uk', 'mongolia', 'hebei china', 'oman', 'prince edward island canada', 'ukraine', 'jiangxi china', 'shaanxi china', 'saint lucia', 'zambia', 'india', 'ningxia china', 'hubei china', 'venezuela', 'pakistan', 'grand princess canada', 'anhui china', 'albania', 'rwanda', 'new caledonia france', 'romania', 'north macedonia', 'sichuan china', 'yunnan china', 'togo', 'russia', 'bulgaria', 'haiti', 'somalia', 'angola', 'mauritania', 'paraguay', 'victoria australia', 'guatemala', 'timor-leste', 'philippines', 'new south wales australia', 'morocco', 'japan', 'nigeria', 'namibia', 'cameroon', 'lebanon', 'mauritius', 'diamond princess canada', 'eswatini', 'ireland', 's. korea', 'germany', 'moldova', 'djibouti', 'channel islands uk', 'brunei', 'sint maarten netherlands', 'uruguay', 'liaoning china', 'british columbia canada', 'dominican republic', 'mexico', 'sri lanka', 'egypt', 'tibet china', 'andorra', 'bolivia', 'guinea', 'slovenia', 'antigua and barbuda', 'shandong china', 'czechia', 'panama', 'switzerland', 'cyprus', 'australian capital territory australia', 'qinghai china', 'chad', 'martinique france', 'seychelles', 'xinjiang china', 'mali', 'georgia', 'brazil', 'curacao netherlands', 'bahrain', 'jamaica', 'western australia australia', 'chile', 'ontario canada', 'estonia', 'argentina', 'saint barthelemy france', 'san marino', 'shanghai china', 'lithuania', 'isle of man uk', 'saint kitts and nevis', 'fujian china', 'belarus', 'diamond princess', 'montenegro', 'iran', 'benin', 'inner mongolia china', 'papua new guinea', 'tunisia', 'senegal', 'taiwan*', 'netherlands', 'indonesia', 'fiji', 'zimbabwe', 'new brunswick canada', 'azerbaijan', 'kuwait', 'poland', 'suriname', 'laos', 'gambia', 'bosnia', 'liberia', 'maldives', 'kyrgyzstan', 'faroe islands denmark', 'sweden', 'dominica', 'bhutan', 'israel', 'grenada', 'saint vincent and the grenadines', 'alberta canada', 'st martin france', 'guinea-bissau', 'colombia', 'equatorial guinea', 'cambodia', 'guangdong china', 'zhejiang china', 'luxembourg', 'croatia', 'singapore', 'slovakia', 'jilin china', 'costa rica', 'montserrat uk', 'burkina faso', 'shanxi china', 'eritrea', 'vietnam', 'hong kong china', 'gabon', 'denmark', 'liechtenstein', 'heilongjiang china', 'newfoundland and labrador canada', 'afghanistan', 'beijing china'}
for e in test:
    if any([substr in e for substr in banned_words]):
        continue

response = requests.get("https://corona.lmao.ninja/v2/historical")
print(response)

countries = []
if response.status_code == 200:
    data = response.json()
    Update(data)
    for i in range(len(data)):
        if data[i]['province'] is not None:
            to_add = data[i]['province'] + " " + data[i]['country']
        else:
            to_add = data[i]['country']
        if not any([substr in to_add for substr in banned_words]):
            countries.append(Country(data[i]))
else:
    print("API ERROR")

jsonFile = open(update_file, "r")
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

globe_data = []
for type in ['c','d']:
    for date in dates:
        series = [date+"_"+type]
        s_data = []
        add = False
        for c in countries:
            s_data.append(round(c.lat))
            s_data.append(round(c.lon))
            if type is 'c':
                val = round(c.cases[date]/Country.maxCases,3)
            else:
                val = round(c.deaths[date]/Country.maxDeaths,3)
            s_data.append(val)
        series.append(s_data)
        globe_data.append(series)


json_globe_data = json.dumps(globe_data)
json_globe_data = json_globe_data.replace("-0.0,","0.000,")
json_globe_data = json_globe_data.replace("0.0,","0.000,")

data_file = "data.json"
jsonFile = open(data_file, "w")
jsonFile.write(json_globe_data)
jsonFile.close()

print("Done")