import os
import re
import string
import codecs
import concurrent.futures
from util import process_source_code
from util import process_srcml_source_code
from util import stripcomments
CURRENT_DIR = os.getcwd()


def pre_process(file_path):
	with codecs.open(file_path,"r",encoding="utf-8", errors="ignore") as f:
		data = f.read()
	try:
		data = str(data)
	except Exception as e:
		print e
	data = process_srcml_source_code(data)
	print(data)

	
	os.remove(file_path)
	with codecs.open(file_path,"a",encoding="utf-8", errors="ignore") as f2:
		f2.write(data)

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"SRCML_PROCESSED_DATA_AFTER_ITERATE_XML")):
		for file in files:
			file_path = os.path.join(r,file)
			print(file_path)
			# with codecs.open(file_path,"r",encoding="utf-8", errors="ignore") as f:
			# 	data = f.read()
			# data = str(data)
			
			future = executor.submit(pre_process,file_path)
			

