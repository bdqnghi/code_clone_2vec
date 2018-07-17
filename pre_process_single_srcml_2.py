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
		# srcml_data_path = os.path.join(CURRENT_DIR,"SRCML_PROCESSED_DATA_VER_2",split[6],split[7])
		# if not os.path.exists(srcml_data_path):
		# 	os.makedirs(srcml_data_path)


		# new_path = os.path.join(CURRENT_DIR,"SRCML_PROCESSED_DATA_VER_2",split[6],split[7],split[8])

		# with codecs.open(new_path,"a",encoding="utf-8", errors="ignore") as f2:
		# 	f2.write(transformed_source_code)
	except Exception as e:
		print "Exeception : " + str(e)


# with open("SRCML_DATA/antlr/cs/ActionLabel.xml", "r")
file_path = "SRCML_DATA/antlr/cs/ActionScriptTarget.xml"

pre_process(file_path,"cs","antlr")


