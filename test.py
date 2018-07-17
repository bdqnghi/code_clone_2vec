
import re

data = "abcDdsadsad dadasdasd"


# Split all camel case
tokens = data.split(" ")
tokens = [x.strip() for x in tokens if x.strip()]

splitted = list()
for token in tokens:
	
	temp = re.sub('(?!^)([A-Z][a-z]+)', r' \1', token).split()

	splitted.extend(temp)
	

data = " ".join(splitted)		

print data