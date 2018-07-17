import os


for r,ds,files in os.walk("./evaluation_data/expressions"):
	for file in files:
		file_path = os.path.join(r,file)
		print(file_path)
		with open(file_path,"r") as f:
			data = f.readlines()
		data = [x.strip() for x in data]
		exprs = list()
		for line in data:
			print line
			elems = line.split(",")
			exprs.append(elems[2])

		# exprs = set(exprs)

		exprs = list(set(exprs))

		outfile = open("./evaluation_data/expressions/" + "list_" + file,"w")
		for item in exprs:
			print item
			outfile.write(item + "\n")
	
