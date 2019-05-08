import json
with open("Boundaries-Community-Areas-current.geojson") as data:
	data = json.load(data)
	newf = open("ca.txt", 'w')
	newf.write("lat_long_dict = {")
	for feature in data["features"]:
		area = feature["properties"]["area_num_1"]
		coords = feature["geometry"]["coordinates"][0][0]
		latavg = 0
		longavg = 0
		total = len(coords)
		
		for pair in coords:
			latavg  += pair[1]
			longavg += pair[0]
		newf.write(area + ': (' + str(latavg/total) + ',' + str(longavg/total) + ')'+',\n')
	newf.write('}')
	newf.close()
