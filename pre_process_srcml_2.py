import os
import re
import string
import codecs
import concurrent.futures
# from util import process_source_code
# from util import process_srcml_source_code
# from util import process_source_code_with_remove_line_break
# from util import stripcomments
from xml_util import transform_source_code
from xml_util import transform_source_code_to_extract_only_api_sequence
CURRENT_DIR = os.getcwd()

# projects = ["cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","aws","mongodb"]
# projects = ["aws"]
projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","itext","jgit","poi","jts","db4o"]

# OUTPUT_FOLDER = "SRCML_PROCESSED_DATA_VER_2"
OUTPUT_FOLDER = "API_SEQUENCES"
def pre_process(file_path,lang,project):
	split = file_path.split("/")
	try:

		# transformed_source_code = transform_source_code(file_path,lang,project)
		transformed_source_code = transform_source_code_to_extract_only_api_sequence(file_path,lang,project)
		transformed_source_code = transformed_source_code.replace("{","").replace("}","").replace("@","")
		transformed_source_code = transformed_source_code.split(" ")
		removed_empty = [x.strip() for x in transformed_source_code if x.strip()]
		transformed_source_code = " ".join(removed_empty)
		
		print transformed_source_code
		srcml_data_path = os.path.join(CURRENT_DIR,OUTPUT_FOLDER,split[6],split[7])
		if not os.path.exists(srcml_data_path):
			os.makedirs(srcml_data_path)


		new_path = os.path.join(CURRENT_DIR,OUTPUT_FOLDER,split[6],split[7],split[8])

		with codecs.open(new_path,"a",encoding="utf-8", errors="ignore") as f2:
			f2.write(transformed_source_code)
	except Exception as e:
		print "Exeception : " + str(e)


for project in projects:
	with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
		for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"SRCML_DATA",project)):
			for file in files:

				file_path = os.path.join(r,file)
				splits = file_path.split("/")

				if splits[7] == "cs" or splits[7] == "java":
					if splits[7] == "cs":
						lang = "cs"
					else:
						lang = "java"
					print file_path
					# with codecs.open(file_path,"r",encoding="utf-8", errors="ignore") as f:
					# 	data = f.read()
					# data = str(data)
					
					future = executor.submit(pre_process,file_path,lang,project)
				

