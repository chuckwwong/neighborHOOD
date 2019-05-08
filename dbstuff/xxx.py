import json
lat_long_dict = {}
with open("Boundaries-Community-Areas-current.geojson") as data:
	data = json.load(data)
	for feature in data["features"]:
		coords = feature["geometry"]["coordinates"][0][0]
		area = feature["properties"]["area_num_1"]
		latavg = 0
		longavg = 0
		total = len(coords)
		for pair in coords:
			latavg  += pair[1]
			longavg += pair[0]
		lat_long_dict[area]= (latavg/total, longavg/total)
for each in lat_long_dict:
	print(lat_long_dict[each])
