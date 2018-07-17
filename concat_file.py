import os
from subprocess import call
import concurrent.futures
# from concurrent.futures import ThreadPoolExecutor
ROOT_URL = "/home/quocnghi/codes/code_clone_w2v"
ORIGINAL_DATA_URL = "/home/quocnghi/codes/code_clone_w2v/PROCESSED_DATA_BACKUP/antlr/java"
# ORIGINAL_DATA_URL = "/home/quocnghi/codes/code_clone_w2v/NEW_DATA"
# pool = ThreadPoolExecutor(30)

for root, dirs, files in os.walk(ORIGINAL_DATA_URL):
	for file in files:
		path = os.path.join(root, file)
		with open(path,"r") as f:
			data=f.readlines()

		for line in data:
			with open("concat_file.txt","a") as f2:
				f2.write(line)
