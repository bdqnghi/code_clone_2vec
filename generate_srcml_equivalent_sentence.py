import os
import codecs
import numpy as np

# from util import process_srcml_source_code

CURRENT_DIR = os.getcwd()

# projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq"]
projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","itext","jgit","poi","jts","db4o","mongodb"]
for project in projects:
	cs_paths = list()
	java_paths = list()
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"SRCML_PROCESSED_DATA_VER_2",project)):
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
				print "File similar : " + cs_file
				try:
					print "##############################"
					with open(cs_path,"r") as cs_f:
						cs_data = str(cs_f.read())
					with open(java_path,"r") as java_f:
						java_data = str(java_f.read())
					cs_data = cs_data.replace("\n","")
					cs_data = cs_data.split(" ")
					cs_data = [x.strip() for x in cs_data if x.strip()]
					# cs_data = " ".join(removed_empty)
					
					java_data = java_data.replace("\n","")
					java_data = java_data.split(" ")
					java_data = [x.strip() for x in java_data if x.strip()]
					# java_data = " ".join(removed_empty)
					
					
					print "Len cs : " + str(len(cs_data))
					print "Len java :" + str(len(java_data))
			
					if len(cs_data) != 0 and len(java_data) !=0:
		

						max_data = max(len(cs_data),len(java_data))
						min_data = min(len(cs_data),len(java_data))

						divide = float(min_data)/float(max_data)
						if divide > 0.6:
						# cs_data = cs_path + " " + cs_data
						# java_data = java_path + " " + java_data
							print cs_file
							print "Because divide = " + str(divide)
							# cs_data = process_srcml_source_code(cs_data)
							# java_data = process_srcml_source_code(java_data)
							cs_data = " ".join(cs_data)
							java_data = " ".join(java_data)
							with open(os.path.join(CURRENT_DIR,"./sentences/sentences_cs_2106.txt"),"a") as f:
								f.write(str(cs_data) + "\n")
							with open(os.path.join(CURRENT_DIR,"./sentences/sentences_java_2106.txt"),"a") as f2:
								f2.write(str(java_data) + "\n")
				except Exception as e:
					print e
					