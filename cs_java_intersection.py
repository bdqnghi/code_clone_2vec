

java_keywords = list()
cs_keywords = list()
with open("java_keywords.txt","r") as f_java:
	j_data = f_java.readlines()
	for line in j_data:
		line = line.replace("\r","").replace("\n","")	
		java_keywords.append(line)


with open("cs_keywords.txt","r") as f_cs:
	cs_data = f_cs.readlines()
	for line in cs_data:
		line = line.replace("\r","").replace("\n","")	
		cs_keywords.append(line)

non_intersect = set(java_keywords).symmetric_difference(cs_keywords)



print non_intersect