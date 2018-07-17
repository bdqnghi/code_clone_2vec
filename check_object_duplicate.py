
objects = list()
with open("./SIGNATURE_DATA/antlr/signature_java.txt","r") as f:
	data = f.readlines()

	for line in data:
		split = line.split(".")
		obj = split[len(split)-2]
		objects.append(obj)
		print obj 

object_set = set(objects)
print len(objects)
print len(object_set)