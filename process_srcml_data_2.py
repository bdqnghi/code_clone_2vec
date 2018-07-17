import os
import re
import string
import codecs
import concurrent.futures


CURRENT_DIR = os.getcwd()
STUPID_URL = "{http://www.srcML.org/srcML/src}"


def pre_process(file_path):

	

	split = file_path.split("/")
	try:
		with open(file_path) as f:
			data = f.read()

		data = str(data)
		data = data.replace("@","")

		data = data.split(" ")
		removed_empty = [x.strip() for x in data if x.strip()]

		processed_code = " ".join(removed_empty)
		os.remove(file_path)


		with codecs.open(file_path,"w",encoding="utf-8", errors="ignore") as f2:
			f2.write(processed_code)

	except Exception as e:
		print(e)
	

with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"SRCML_PROCESSED_DATA_VER_2")):
		for file in files:
			if file.endswith(".xml"):
				file_path = os.path.join(r,file)
				print(file_path)
				# with codecs.open(file_path,"r",encoding="utf-8", errors="ignore") as f:
				# 	data = f.read()
				# data = str(data)
				pre_process(file_path)
				# future = executor.submit(pre_process,file_path)
