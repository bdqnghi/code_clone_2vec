import os
import codecs
import numpy as np
from shutil import copyfile



CURRENT_DIR = os.getcwd()

# projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","aws","mongodb"]
# projects = ["itext","jgit","poi","jts","db4o"]
projects = ["antlr"]

for project in projects:
	count = 0
	cs_paths = list()
	java_paths = list()
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"PROCESSED_DATA_BACKUP_ORIGINAL",project)):
		for file in files:
			file_path = os.path.join(r,file)
			split = file_path.split("/")
			if split[7] == "cs":
				cs_paths.append(file_path)
			if split[7] == "java":
				java_paths.append(file_path)


	for cs_path in cs_paths:
		for java_path in java_paths:
			cs_splits = cs_path.split("/")
			java_splits = java_path.split("/")
			cs_file = cs_splits[8]
			java_file = java_splits[8]
			if cs_file.split(".")[0] == java_file.split(".")[0]:
				print cs_path
				count += 1
				copyfile(cs_path, "/home/nghibui/codes/code_clone_w2v/TEMP_CS/" + cs_path.split("/")[8])
			# 	line = project + "," + cs_path + "," + java_path
			# 	with open(os.path.join(CURRENT_DIR,"similar_files.txt"),"a") as f:
			# 		f.write(str(line) + "\n")
			# 
	# print project + " : " + str(count)