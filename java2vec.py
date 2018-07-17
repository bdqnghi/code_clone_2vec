import gensim
import os
import codecs
from sklearn.manifold import TSNE
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.getcwd()

def load_embeddings(file_name):
	with codecs.open(file_name,"r","utf-8") as f:
		next(f)
		vocabulary, wv = zip(*[line.strip().split(" ",1) for line in f])
	wv = np.loadtxt(wv)
	return wv,vocabulary

# java_sentences = list()
# for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"PROCESSED_DATA")):
# 	for file in files:
# 		file_path = os.path.join(r,file)
# 		if file.endswith(".java"):
# 			with open(file_path,"r") as f:
# 				data = f.read()
# 			sentence = data.split(" ")
			
# 			java_sentences.append(sentence)

print "Building Word2Vec model......."
# model = gensim.models.Word2Vec(java_sentences,min_count=30,size=100,workers=6,iter=30,sg=1,window=7)

# model.save("java2vec")

# model = gensim.models.Word2Vec.load("java2vec")

# model.wv.save_word2vec_format("java2vec.txt",fvocab=None,binary=False)
# print model.similarity("system","namespace")

# word_vectors = KeyedVectors.load_word2vec_format("java2vec",binary=True)

# print word_vectors

wv,vocabulary = load_embeddings("java2vec.txt")

print type(vocabulary)
tsne = TSNE(n_components=2, random_state=0)

np.set_printoptions(suppress=True)
Y = tsne.fit_transform(wv[:200,:])

plt.scatter(Y[:,0],Y[:,1])
for label, x, y in zip(vocabulary,Y[:,0],Y[:,1]):
	plt.annotate(label,xy=(x,y),xytext=(0,0),textcoords="offset points")

plt.show()
