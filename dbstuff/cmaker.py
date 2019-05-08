empty = []
with open("crimes.json") as c:
	file = c.readlines()
	for line in file:
		if line == file[-1]:
			empty.append(line)
		else:
			empty.append(line+',')
newf = open("crimetotal.json", 'w')
newf.write('{"crimes":[')
for line in empty:
	newf.write(line)
newf.write("]}")
newf.close()
