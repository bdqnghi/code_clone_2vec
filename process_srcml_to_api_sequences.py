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

projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","itext","jgit","poi","jts","db4o"]
for project in projects:
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"SRCML_PROCESSED_DATA_VER_2",project)):
		for file in files:

			file_path = os.path.join(r,file)
			splits = file_path.split("/")
			print(file_path)

			with open(file_path, "r") as f:
				data = f.read()
			

			tokens = data.split(" ")

			api_tokens = []
			for token in tokens:
				if "." in token and "(" in token:
					api_tokens.append(token)


			splits[5] = "API_SEQUENCES"
			api_sequence_folder_path = "/".join(splits[:8])
			if not os.path.exists(api_sequence_folder_path):
				os.makedirs(api_sequence_folder_path)


			new_file_path = "/".join(splits[:8]) + "/" + file

			with codecs.open(new_file_path,"a",encoding="utf-8", errors="ignore") as f2:
				f2.write(" ".join(api_tokens))