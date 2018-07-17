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
from util import vector_summing
from util import vector_summing_with_tfidf
import operator
from sklearn.metrics.pairwise import euclidean_distances
import sys
from tqdm import *
import random
csv.field_size_limit(sys.maxsize)
DIMENSION = 25
PROJECT = "antlr"
RANDOM_RANGE = 37
cs_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/cs_vectors_11_25.txt",binary=False)
java_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/java_vectors_11_25.txt",binary=False)

# cs_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/cs_vectors_10_25_include_functions.txt",binary=False)
# java_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/java_vectors_10_25_include_functions.txt",binary=False)

smallprojects = ["factual","mongodb","log4j","datastax"]
with open("./sentences/sentences_cs_11.txt","r") as cs_f:
	cs_data = cs_f.readlines()
with open("./sentences/sentences_java_11.txt","r") as java_f:
	java_data = java_f.readlines()

cs_sentences = [x for x in cs_data]
java_sentences = [x for x in java_data]

cs_word2weight = word2weight(cs_sentences)
java_word2weight = word2weight(java_sentences)


def get_random_range(project):
	if project == "fpml":
		return 527
	if project == "antlr":
		return 2019
	if project =="factual":
		return 95
	if project == "lucene":
		return 7720
	if project == "mongodb":
		return 65
	if project == "spring":
		return 352
	if project == "log4j":
		return 50
	if project == "zeromq":
		return 199
	if project =="datastax":
		return 37
	if project == "aws":
		return 532
	else:
		return 100
#---------------To evaluate pairwise---------------------
# with codecs.open("./evaluation_data/pairs.csv","r") as f_csv:
# 	reader = csv.reader(f_csv)

# 	for i,row in enumerate(reader):
# 		if i != 0:
# 			print "#########################"
# 			print row[3]

# 			expr_cs = row[3]
# 			expr_java = row[2]
# 			expr_cs = process_expression(expr_cs,1)
# 			expr_java = process_expression(expr_java,0)
# 			print expr_cs

# 			predict_average = cosine_similarity(vector_averaging(expr_cs.split(" "),cs_vectors,DIMENSION),vector_averaging(expr_java.split(" "),java_vectors,DIMENSION))[0][0]
# 			predict_average_tfidf = cosine_similarity(vector_averaging_with_tfidf(expr_cs.split(" "),cs_vectors,cs_word2weight,DIMENSION),vector_averaging_with_tfidf(expr_java.split(" "),java_vectors,java_word2weight,DIMENSION))[0][0]
# 			print predict_average
# 			print predict_average_tfidf
# 			new_row = list()
# 			new_row.append(expr_java)
# 			new_row.append(expr_cs)
# 			new_row.append(str(predict_average))
# 			new_row.append(str(predict_average_tfidf))
# 			with open("./evaluation_result/expression_result_8.csv","a") as f:
# 				f.write(",".join(new_row) + "\n")


#---------------To evaluate top k---------------------

def get_top_k_match(k, source, targets, source_embeddings,target_embeddings ):

	result_dict_average = {}
	result_dict_average_tfidf = {}
	result_dict_sum = {}
	for t in targets:
	
	
		distance_average = euclidean_distances(vector_averaging(source.split(" "),source_embeddings,DIMENSION),vector_averaging(t.split(" "),target_embeddings,DIMENSION))[0][0]
		distance_average_tfidf = euclidean_distances(vector_averaging_with_tfidf(source.split(" "),source_embeddings,cs_word2weight,DIMENSION),vector_averaging_with_tfidf(t.split(" "),target_embeddings,java_word2weight,DIMENSION))[0][0]
		# distance_sum = euclidean_distances(vector_summing(source.split(" "),source_embeddings,DIMENSION),vector_summing(t.split(" "),target_embeddings,DIMENSION))[0][0]
		# distance_sum_tfidf = euclidean_distances(vector_summing_with_tfidf(source.split(" "),source_embeddings,cs_word2weight,DIMENSION),vector_averaging_with_tfidf(t.split(" "),target_embeddings,java_word2weight,DIMENSION))[0][0]
		
		result_dict_average[t] = distance_average
		result_dict_average_tfidf[t] = distance_average_tfidf
		# result_dict_sum[t] = distance_sum
	

	sorted_result_average = sorted(result_dict_average.items(), key=operator.itemgetter(1))

	
	sorted_result_average_tfidf = sorted(result_dict_average_tfidf.items(), key=operator.itemgetter(1))

	
	# sorted_result_sum = sorted(result_dict_sum.items(), key=operator.itemgetter(1))
	return sorted_result_average[:k], sorted_result_average_tfidf[:k] #sorted_result_sum[:k]

with open("./evaluation_data/expressions/ground_truth_expression_antlr_1.csv","r") as f_csv:
	reader = csv.reader(f_csv)
	java_phrases = list()
	cs_phrases = list()
	mapping_java = {}
	mapping_cs = {}

	cs_queries = list()
	java_queries = list()
	for i,row in tqdm(enumerate(reader)):
		if i != 0:
			# print "#########################"

			expr_cs = row[2]
			# print expr_cs
			# expr_cs = process_expression(expr_cs,1)

			# print expr_cs
			expr_java = row[3]
			# expr_java = process_expression(expr_java,0)
			java_queries.append(expr_java)
			cs_queries.append(expr_cs)

			# java_phrases.append(expr_java)
			# cs_phrases.append(expr_cs)
			mapping_java[expr_java] = expr_cs
			mapping_cs[expr_cs] = expr_java

	with open("./evaluation_data/expressions/list_expressions_cs_" + PROJECT + "_1.csv","r") as f_cs:
		cs_temp = f_cs.readlines()
		cs_data = [x.strip() for x in cs_temp]
	for c in cs_data:
		cs_phrases.append(c)

	with open("./evaluation_data/expressions/list_expressions_java_" + PROJECT + "_1.csv","r") as f_java:
		java_temp = f_java.readlines()
		java_data = [x.strip() for x in java_temp]
	for j in java_data:
		java_phrases.append(j)

	print "Finish processing ......"

	for a in range(1):
		print "Iteration number : " + str(a) + "-----------------"
		avg_p_list_cs_average = list()
		avg_p_list_cs_average_tfidf = list()
		avg_p_list_cs_sum = list()
		# print cs_phrases
		
		# random_list = random.sample(range(0, get_random_range(PROJECT)), 100)

		# random_list = [x for x in range(0,RANDOM_RANGE)]
		# random_cs_phrases = list()
		# for i,temp in enumerate(cs_phrases):
		# 	if i in random_list:
		# 		random_cs_phrases.append(temp)

		print "Finish getting random list ....."

		print "CS part ...."
		for i,cs_k in tqdm(enumerate(cs_queries)):
			# print "############################"
			
			try:
				
				top_k_java_average, top_k_java_average_tfidf = get_top_k_match(5,cs_k,java_phrases,cs_vectors,java_vectors)
			
				relevant_list_average = list()
				relevant_list_average_tfidf = list()
				relevant_list_sum = list()
				# print cs_k

				print top_k_java_average
				for element in top_k_java_average:
					
					if element[0] in mapping_java:
						if mapping_java[element[0]] == cs_k:
							relevant_list_average.append(1)
						else:
							relevant_list_average.append(0)
					else:
						relevant_list_average.append(0)
				# avg_p =  average_precision(relevant_list)
				
				avg_p_list_cs_average.append(relevant_list_average)
				
				
				for element in top_k_java_average_tfidf:
					if element[0] in mapping_java:
						if mapping_java[element[0]] == cs_k:
							relevant_list_average_tfidf.append(1)
						else:
							relevant_list_average_tfidf.append(0)
					else:
						relevant_list_average_tfidf.append(0)
				# avg_p =  average_precision(relevant_list_tfidf)
				avg_p_list_cs_average_tfidf.append(relevant_list_average_tfidf)

				# for element in top_k_java_sum:
					
				# 	if mapping_java[element[0]] == cs_k:
				# 		relevant_list_sum.append(1)
				# 	else:
				# 		relevant_list_sum.append(0)
				# # avg_p =  average_precision(relevant_list_tfidf)
				# avg_p_list_cs_sum.append(relevant_list_sum)
				
			except Exception as e:
				print "Error is :" + str(e)

		print avg_p_list_cs_average
		print avg_p_list_cs_average_tfidf
		map_cs_average = "MAP CS average: " + str(mean_average_precision(avg_p_list_cs_average))
		map_cs_average_tfidf = "MAP CS average tfidf: " + str(mean_average_precision(avg_p_list_cs_average_tfidf))
		# print "MAP CS sum: " + str(mean_average_precision(avg_p_list_cs_sum))

		with open("./evaluation_result/expressions/expression_result_average_" + PROJECT + "_11_25_1" + ".csv","a") as f:
			f.write("Iteration : " + str(a) + " --------------"  + "\n")


		with open("./evaluation_result/expressions/expression_result_average_" + PROJECT + "_11_25_1" + ".csv","a") as f:
			f.write(map_cs_average + "\n")


			f.write(map_cs_average_tfidf + "\n")

		# Java part -----------------------

		# print "Now the Java part ...."
		# avg_p_list_java_average = list()
		# avg_p_list_java_average_tfidf = list()
		# avg_p_list_java_sum = list()

		# random_java_phrases = list()
		# for i,temp in enumerate(java_phrases):
		# 	if i in random_list:
		# 		random_java_phrases.append(temp)


		# for i,java_k in tqdm(enumerate(random_java_phrases)):
		
		# 	try:

		# 		# print java_k
		# 		# top_5_cs = cs_vectors.similar_by_vector(java_vectors[java_k], topn=3)
		# 		top_k_cs_average,top_k_cs_average_tfidf = get_top_k_match(1,java_k,cs_phrases,java_vectors,cs_vectors)
		# 		# print top_5_cs
		# 		relevant_list_average = list()
		# 		relevant_list_average_tfidf = list()
		# 		relevant_list_sum = list()
				
		# 		for element in top_k_cs_average:
		# 			if mapping_cs[element[0]] == java_k:
		# 				relevant_list_average.append(1)
		# 			else:
		# 				relevant_list_average.append(0)
			
		# 		# avg_p =  average_precision(relevant_list)
		# 		avg_p_list_java_average.append(relevant_list_average)
				
		# 		for element in top_k_cs_average_tfidf:
					
		# 			if mapping_cs[element[0]] == java_k:
					
		# 				relevant_list_average_tfidf.append(1)
		# 			else:
				
		# 				relevant_list_average_tfidf.append(0)
		# 		# avg_p =  average_precision(relevant_list_tfidf)
		# 		avg_p_list_java_average_tfidf.append(relevant_list_average_tfidf)

		# 	except Exception as e:

		# 		print e

		# print "Calculating MAP for Java part ..........."
		# # print avg_p_list_java
		# map_java_average =  "MAP Java average : " + str(mean_average_precision(avg_p_list_java_average))
		# map_java_average_tfidf = "MAP Java average tfidf: " + str(mean_average_precision(avg_p_list_java_average_tfidf))

		# with open("./evaluation_result/function_result_average_" + PROJECT + "_11_25_1" + ".csv","a") as f:
		# 	f.write(map_java_average + "\n")
		# 	f.write(map_java_average_tfidf + "\n")

		# # print "Finish " + str(a) + " iteration----------------"
