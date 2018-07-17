import gensim
import os
import codecs
from sklearn.manifold import TSNE
from gensim.models.keyedvectors import KeyedVectors
from util import check_if_token_is_method_signature
from util import check_if_token_is_object_signature

URL = "./usage_mapping_evaluation/" + "sdk_method_usage_mapping_java.txt"
project = "sdk"
cs_packages = ["System."]
java_packages = ["java.","javax."]


# project = "lucene"
# cs_packages = ["Lucene."]
# java_packages = ["lucene.","solr."]

# project = "db4o"
# cs_packages = ["Db4objects.","Db4oUnit"]
# java_packages = ["db4o."]

usage_type = "method"

with open(URL,"r") as f:
	data = f.readlines()

keys = list()
for line in data:
	line = line.strip()
	splits = line.split("-")
	keys.append(splits[0])

cs_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/cs_vectors_global_local.txt",binary=False)
java_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/java_vectors_global_local.txt",binary=False)

for key in keys:
	try:
		vector = java_vectors[key]
		k_nearest= cs_vectors.similar_by_vector(vector, topn=50)
		relevant_k = list()

		for k in k_nearest:
			if check_if_token_is_method_signature(k[0]) == True:

				# if check_package_include(java_packages,k[0]) == True:
				relevant_k.append(k[0])

		if len(relevant_k) != 0:
					
			outpur_cs_url = "./usage_mapping_evaluation/" + project + "_" + usage_type + "_usage_mapping_java_global_local.txt"
			
			if len(relevant_k) != 0:
				with open(outpur_cs_url,"a") as f1:
					f1.write(key + "-" + "__".join(relevant_k) + "\n")
	except Exception as e:
		print e