import gensim
import os
import codecs
from sklearn.manifold import TSNE
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
import csv
from sklearn.metrics.pairwise import cosine_similarity
import sys
from sklearn.neighbors import NearestNeighbors
from util import check_if_token_is_method_signature
from util import check_if_token_is_object_signature

# project = "antlr"
# cs_package = "Antlr3."
# java_package = "antlr."

def check_package_include(packages,text):
	
	check = False
	for package in packages:
		if package in text:
			check = True
	return check

project = "all_sdk"

usage_type = "method"

if usage_type == "method":
	func = check_if_token_is_method_signature
else:
	func = check_if_token_is_object_signature

with open("./bi2vec_vectors/cs_vectors_new.txt") as cs_f:
	# next(cs_f)
	cs_embeddings = cs_f.readlines()

with open("./bi2vec_vectors/java_vectors_new.txt") as java_f:
	# next(java_f)
	java_embeddings = java_f.readlines()

cs_signature_tokens = list()
java_signature_tokens = list()

for cs_emb in cs_embeddings:
	split = cs_emb.split(" ")
	if func(split[0]) == True:
		if "System." in split[0]:
			cs_signature_tokens.append(split[0])

print "cs tokens : " + str(len(cs_signature_tokens))

for java_emb in java_embeddings:
	split = java_emb.split(" ")
	if func(split[0]) == True:	
		if "java." in split[0] or "javax." in split[0]:	
			java_signature_tokens.append(split[0])

print "java tokens : " + str(len(java_signature_tokens))
print "Loading word embedding..........."
cs_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/cs_vectors_new.txt",binary=False)
java_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/java_vectors_new.txt",binary=False)

print "Finish loading.............."
# print cs_vectors.similar_by_vector(java_vectors["java.util.concurrent.locks.Lock.lock()"], topn=30)
# print cs_vectors.similar_by_vector(java_vectors["package"], topn=30)


for cs_token in cs_signature_tokens:
	split = cs_token.split(".")
	method_source = split[len(split)-1].split("(")[0]

	k_nearest = java_vectors.similar_by_vector(cs_vectors[cs_token], topn=50)
	relevant_k = list()
	for k in k_nearest:
		if func(k[0]) == True:	
			# split = k[0].split(".")
			# method_target = split[len(split) - 1].split("(")[0]
			# print "comparing : " + method_source + " vs " + method_target
			# if method_target.lower() == method_source.lower(): 	
			relevant_k.append(k[0])


	if len(relevant_k) != 0:
		with open("./usage_mapping/" + project + "_" + usage_type + "_usage_mapping_cs.txt","a") as f1:
			f1.write(cs_token + "-" + "__".join(relevant_k) + "\n")
			# f1.write(cs_token + "-" + relevant_k[0] + "\n")

for java_token in java_signature_tokens:
	split = java_token.split(".")
	method_source = split[len(split)-1].split("(")[0]
	k_nearest = cs_vectors.similar_by_vector(java_vectors[java_token], topn=50)
	relevant_k = list()
	for k in k_nearest:
		if func(k[0]) == True:
			

			# split = k[0].split(".")
			# method_target = split[len(split) - 1].split("(")[0]
		
			# print "comparing : " + method_source + " vs " + method_target
			# if method_target.lower() == method_source.lower(): 
			
			relevant_k.append(k[0])

	if len(relevant_k) != 0:
		with open("./usage_mapping/" + project + "_" + usage_type + "_usage_mapping_java.txt","a") as f1:
			f1.write(java_token + "-" + "__".join(relevant_k) + "\n")
			# f1.write(java_token + "-" + relevant_k[0] + "\n")