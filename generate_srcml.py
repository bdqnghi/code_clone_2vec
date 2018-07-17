import os
from subprocess import call
import concurrent.futures

ROOT_URL = "/home/quocnghi/codes/code_clone_w2v"
ROOT_URL = "/home/quocnghi/codes/code_clone_w2v"
# ORIGINAL_DATA_URL = "/home/quocnghi/codes/code_clone_w2v/PROCESSED_DATA_BACKUP_ORIGINAL"
ORIGINAL_DATA_URL = "/home/quocnghi/codes/code_clone_w2v/PROCESSED_DATA_BACKUP_ORIGINAL"
# pool = ThreadPoolExecutor(30)
# projects = ["itext","jgit","poi","jts","db4o"]
projects = ["antlr"]
def execute_command(build_project_command):
	try:
		print(build_project_command)
		# os.system(build_project_command)
	except Exception as e:
		print(e)

with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
	for project in projects:
		for root, dirs, files in os.walk(os.path.join(ORIGINAL_DATA_URL,project)):
			for file in files:

				
				file_path = os.path.join(root,file)
				
				split = file_path.split("/")
			
				project_name = split[6]
				project_lang = split[7]
				srcml_data_path = os.path.join(ROOT_URL,"SRCML_DATA",project_name,project_lang)
				if not os.path.exists(srcml_data_path):
					os.makedirs(srcml_data_path)
				srcml_path = os.path.join(srcml_data_path,str(file).split(".")[0] + ".xml")
				print(srcml_path)
				# project_path 	
				generate_srcml_command = "srcml " + file_path + " > " + srcml_path
				try:
					future = executor.submit(execute_command, generate_srcml_command)
				except Exception as e:
					print(e)