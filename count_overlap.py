# This file is to count overlap between StaMiner result and our result

import csv
import collections

statminer_list = []
our_list = []

with open("FoundUnmappedPairs.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        # print(row[0])

        # signature_split = row[0].split(".")
        s = row[0].split("(")[0]
        # join_split = ".".join(signature_split)
        statminer_list.append(s)
        # print(row[0])
        # print(row[0],row[1],row[2],)

with open("./SIGNATURE_DATA/sdk/signature_java.txt") as file:
	data = file.readlines()
	for line in data:
		s = line.replace("\n","").replace("\t","")
		our_list.append(s.split("(")[0])

# print(statminer_list)
# print(our_list)

# print(set(our_list).isdisjoint(statminer_list))


a_multiset = collections.Counter(statminer_list)
b_multiset = collections.Counter(our_list)

overlap = list((a_multiset & b_multiset).elements())

print(overlap)
print(len(overlap))