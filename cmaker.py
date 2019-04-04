empty = []
with open("crime1.json") as c1:
	file = c1.readlines()
	for line in file:
		empty.append(line+',')
with open("crime2.json") as c2:
	file = c2.readlines()
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
