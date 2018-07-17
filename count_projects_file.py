
import os
import codecs

import numpy as np


CURRENT_DIR = os.getcwd()

# projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq"]

# projects = ["mysql","protobuf","mongodb","rabbitmq"]
projects = ["antlr","lucene","spring","datastax","db4o","fpml","itext","jgit","jts","log4j","poi","zeromq"]
# projects = ["db4o"]
# DIRECTORY = "PROCESSED_DATA_BACKUP_ORIGINAL"
DIRECTORY = "PROJECT_DATA_RAW"
for project in projects:
	cs_paths = list()
	java_paths = list()
	num_cs = 0
	num_java = 0
	overlap = 0
	print "####################"
	print "Project : " + project
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,DIRECTORY,project)):
		
		for file in files:
			file_path = os.path.join(r,file)
			if file.endswith(".cs"):
				cs_paths.append(file_path)
				num_cs +=1
			if file.endswith(".java"):
				java_paths.append(file_path)
				num_java +=1
	print "num cs  :" + str(num_cs)
	print "num java  :" + str(num_java)

	for cs_path in cs_paths:
		for java_path in java_paths:
			cs_splits = cs_path.split("/")
			java_splits = java_path.split("/")

			cs_file = cs_splits[len(cs_splits)-1]
			java_file = java_splits[len(java_splits)-1]
			# print java_file
			if cs_file.split(".")[0] == java_file.split(".")[0]:
				# print cs_file
				# print(cs_file)
				# print(java_file)
				overlap += 1

	print "overlap : " + str(overlap)