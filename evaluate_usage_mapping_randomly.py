import random
from random import randint

# project = "sdk"
# project = "jgit"
# project = "itext"
# project = "jts"
# project = "lucene"
# project = "jgit"
project = "db4o"
usage_type = "method"
lang = "java"


URL = "./usage_mapping/" + project + "_" + usage_type + "_usage_mapping_" + lang + ".txt"

URL_EVAL = "./usage_mapping_evaluation/" + project + "_" + usage_type + "_usage_mapping_" + lang + ".txt"

with open(URL,"r") as f:
	data = f.readlines()

print len(data)
random_row = random.sample(range(0,len(data)-1),100)

count = 0
consider_rows = list() 
for line in data:
	usage = line.strip()
	# splits = usage.split("-")

	if count in random_row:
		# consider_rows.append(usage)
		with open(URL_EVAL,"a") as f2:
			f2.write(usage + "\n")
	count += 1 
