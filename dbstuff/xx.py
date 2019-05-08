import json
with open("Boundaries-Community-Areas-current.geojson") as data:
	data = json.load(data)
	newf = open("ca.txt", 'w')
	for feature in data["features"]:
		area = feature["properties"]["area_num_1"]
		community = feature["properties"]["community"]
		coords = feature["geometry"]["coordinates"][0][0]

		newf.write('{ \nid: ' + area + ',' + '\nname: "' + community +'",'+ '\nopacity: 0.5,' +"\npaths: [\n")
		flag = 0
		latavg = 0
		longavg = 0
		total = len(coords)
		for pair in coords:
			p1 = str(pair[1])
			p2 = str(pair[0])
			latavg  += pair[1]
			longavg += pair[0]
			
			if pair != coords[-1] or not flag:
				if not flag:
					flag = 1
				newf.write('{lat: ' + p1 + ', lng: ' + p2 + "},\n")
			else:
				newf.write('{lat: ' + p1 + ', lng: ' + p2 + "}")
		
		newf.write("\n],\n" + "mlat: " + str(latavg/total).lstrip('+') + ",\n mlong: " + str(longavg/total) + "\n},\n")
		print(str(latavg/total), str(longavg/total))
	newf.close()
