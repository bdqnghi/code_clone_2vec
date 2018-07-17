import gensim
import os
import codecs
from sklearn.manifold import TSNE
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
from util import vector_averaging
from util import vector_averaging_with_tfidf
from sklearn.metrics.pairwise import cosine_similarity
from util import word2weight
csv.field_size_limit(sys.maxsize)

def load_embeddings(file_name):
	with codecs.open(file_name,"r","utf-8") as f:
		next(f)
		vocabulary, wv = zip(*[line.strip().split(" ",1) for line in f])
	wv = np.loadtxt(wv)
	return wv,vocabulary

# with open("sentences_cs_5.txt","r") as cs_f:
# 	cs_data = cs_f.readlines()
# with open("sentences_java_5.txt","r") as java_f:
# 	java_data = java_f.readlines()

# cs_sentences = [x for x in cs_data]
# java_sentences = [x for x in java_data]

# cs_word2weight = word2weight(cs_sentences)
# java_word2weight = word2weight(java_sentences)

cs_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/cs_vectors_10_25_include_functions.txt",binary=False)
java_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/java_vectors_10_25_include_functions.txt",binary=False)

words = ("if","else","while","for","int","public","private","void","get","set","float","http","do","break","double","enum")
# words = ("public","string","if","double","float","else","while","+","=","-","==","+=","int","private","for","throw","catch","try","identifier","expr","function","function_decl")
# words = ("public","if","else","while","private","float","double")
# words = ("for","public","class")
# phrases = ("identifier = identifer + identifier","identifier += identifer","identifier = identifer - identifier","identifier -= identifer","identifier == identifier", "identifier != identifier")

def get_words(words,word2vec):	
	s_word2vec = list()
	for word in words:
		s_word2vec.append(word2vec[word])
	return np.array(s_word2vec)

def generate_cs_labels(words):
	both = list()
	for word in words:
		both.append(word + "(cs)")
	return tuple(both)

def generate_java_labels(words):
	both = list()

	for word in words:
		both.append(word + "(java)")
	return tuple(both)

def generate_both_labels(words):
	both = list()
	for word in words:
		both.append(word + "(cs)")
	for word in words:
		both.append(word + "(java)")
	return tuple(both)

def print_pair_cosine_similarity(words,cs_vectors,java_vectors):
	for word in words:
		for word2 in words:
			with open("cosine_sim.csv","a") as f:
				
				line = "'" + word + "'" + "," + "'" + word2 + "'" + "," + str(cosine_similarity(cs_vectors[word].reshape(1,-1),java_vectors[word2].reshape(1,-1))[0][0])
				f.write(line + "\n")

def print_phrase_cosine_similarity(phrases,cs_vectors,java_vectors):
	for p in phrases:
		for p2 in phrases:
			cs_vec = vector_averaging(p.split(" "),cs_vectors)
			java_vec = vector_averaging(p2.split(" "),java_vectors)

			# cs_vec_tfidf = vector_averaging_with_tfidf(p.split(" "),cs_vectors,cs_word2weight)
			# java_vec_tfidf = vector_averaging_with_tfidf(p.split(" "),java_vectors,java_word2weight)

			cos_sim = cosine_similarity(cs_vec,java_vec)[0][0]
			# cos_sim_tfidf = cosine_similarity(cs_vec_tfidf,java_vec_tfidf)[0][0]

			with open("cosine_sim_phrase.csv","a") as f:
				line = p + "," + p2 + "," + str(cos_sim)
				f.write(line + "\n")
# java_wv,java_vocabulary = load_embeddings("./bi2vec_vectors/java_vectors.txt")

# cs_wv,cs_vocabulary = load_embeddings("./bi2vec_vectors/cs_vectors.txt")
# print_pair_cosine_similarity(words,cs_vectors,java_vectors)
# print_phrase_cosine_similarity(phrases,cs_vectors,java_vectors)

# exit()
tsne = TSNE(n_components=2, random_state=0)
tsne_java = TSNE(n_components=2, random_state=0)
tsne_cs = TSNE(n_components=2, random_state=0)

words_java_wv = get_words(words,java_vectors)
words_cs_wv = get_words(words,cs_vectors)
words_both_wv = np.concatenate([words_cs_wv,words_java_wv])

words_both = generate_both_labels(words)
words_java = generate_java_labels(words)
words_cs = generate_cs_labels(words)
np.set_printoptions(suppress=True)

# Y_java = tsne_java.fit_transform(words_java_wv)

# plt.scatter(Y_java[:,0],Y_java[:,1],color="red")
# for label, x, y in zip(words_java,Y_java[:,0],Y_java[:,1]):
# 	plt.annotate(label,xy=(x,y),xytext=(0,0),textcoords="offset points",color="red")


# Y_cs = tsne_cs.fit_transform(words_cs_wv)

# plt.scatter(Y_cs[:,0],Y_cs[:,1],color="blue")
# for label, x, y in zip(words_cs,Y_cs[:,0],Y_cs[:,1]):
# 	plt.annotate(label,xy=(x,y),xytext=(0,0),textcoords="offset points",color="blue")

Y_both = tsne.fit_transform(words_both_wv)
print type(Y_both)
print Y_both[:,0]
print Y_both[:,1]
print Y_both
plt.scatter(Y_both[:,0],Y_both[:,1])
for label, x, y in zip(words_both,Y_both[:,0],Y_both[:,1]):
	color = "blue"
	if "cs" in label:
		color = "red"
	
	plt.annotate(label,xy=(x,y),xytext=(0,0),textcoords="offset points",color=color)


plt.show()
