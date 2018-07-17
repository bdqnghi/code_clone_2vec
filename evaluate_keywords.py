import gensim
import os
import codecs
from sklearn.manifold import TSNE
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
import csv
from sklearn.metrics.pairwise import cosine_similarity
from util import vector_averaging
from util import vector_averaging_with_tfidf
from util import process_source_code
from util import process_diff_srcml
from util import process_diff_srcml2
from util import word2weight
from util import process_expression
from util import mean_average_precision
from util import average_precision
from util import precision_at_k
import sys

DIMENSION = 20
cs_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/cs_vectors_11_20.txt",binary=False)
java_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/java_vectors_11_20.txt",binary=False)

with open("./sentences/sentences_cs_11.txt","r") as cs_f:
	cs_data = cs_f.readlines()
with open("./sentences/sentences_java_11.txt","r") as java_f:
	java_data = java_f.readlines()

cs_sentences = [x for x in cs_data]
java_sentences = [x for x in java_data]

cs_word2weight = word2weight(cs_sentences)
java_word2weight = word2weight(java_sentences)


with codecs.open("./evaluation_data/keywords.csv","r") as f_csv:
	reader = csv.reader(f_csv)
	java_keywords = list()
	cs_keywords = list()
	mapping_java = {}
	mapping_cs = {}
	for i,row in enumerate(reader):
		if i != 0:
			# print "#########################"
			expr_cs = row[1].strip("\"")
			expr_java = row[2].strip("\"")
			java_keywords.append(expr_java)
			cs_keywords.append(expr_cs)
			mapping_java[expr_java] = expr_cs
			mapping_cs[expr_cs] = expr_java

	# precision_list_java = list()
	# avg_p_list_java = list()
	# for java_k in java_keywords:
	# 	if java_k == "for" or java_k =="interface" or java_k == ">>>" or java_k == ":" or java_k == "implements" or java_k == "extends":
	# 		continue
	# 	print "############################"
	# 	try:
	# 		print java_k
	# 		top_5_cs = cs_vectors.similar_by_vector(java_vectors[java_k], topn=10)
	# 		print top_5_cs
	# 		relevant_list = list()
			
	# 		for element in top_5_cs:
	# 			if element[0] == java_k:
	# 				relevant_list.append(1)
	# 			elif element[0] == mapping_java[java_k]:
	# 				relevant_list.append(1)
	# 			elif java_k == "final" and element[0] == "readonly":
	# 				relevant_list.append(1)
	# 			else:
	# 				relevant_list.append(0)
			
	# 		if 1 in relevant_list:
	# 			print "Relevant"
	# 		else:
	# 			print "Not relevant"
	# 		avg_p =  average_precision(relevant_list)
	# 		avg_p_list_java.append(relevant_list)
	# 		# print avg_p
	# 		precision_list_java.append(avg_p)
	# 	except Exception as e:
	# 		print e

	# print avg_p_list_java
	# print "MAP Java : " + str(mean_average_precision(avg_p_list_java))

	
	# precision_list_cs = list()
	# avg_p_list_cs = list()
	# for cs_k in cs_keywords:
	# 	# print "############################"
	# 	try:
	# 		# print cs_k
	# 		top_5_java = java_vectors.similar_by_vector(cs_vectors[cs_k], topn=5)
	# 		# print top_5_java
	# 		relevant_list = list()
			
	# 		for element in top_5_java:
	# 			if element[0] == cs_k:
	# 				relevant_list.append(1)
	# 			else:
	# 				relevant_list.append(0)
	# 		avg_p =  average_precision(relevant_list)
	# 		avg_p_list_cs.append(relevant_list)
	# 		# print avg_p
	# 		precision_list_cs.append(avg_p)
	# 	except Exception as e:
	# 		print e

	# print avg_p_list_cs
	# print "MAP CS : " + str(mean_average_precision(avg_p_list_cs))


			print expr_cs
			print expr_java
			predict_average = cosine_similarity(vector_averaging(expr_cs.split(" "),cs_vectors,DIMENSION),vector_averaging(expr_java.split(" "),java_vectors,DIMENSION))[0][0]
			predict_average_tfidf = cosine_similarity(vector_averaging_with_tfidf(expr_cs.split(" "),cs_vectors,cs_word2weight,DIMENSION),vector_averaging_with_tfidf(expr_java.split(" "),java_vectors,java_word2weight,DIMENSION))[0][0]
			
			new_row = list()

			new_row.append(str(predict_average))
			new_row.append(str(predict_average_tfidf))
			with open("./evaluation_result/keywords_result_11_20_include_functions.csv","a") as f:
				f.write(",".join(new_row) + "\n")