import gensim
import os
import codecs
from sklearn.manifold import TSNE
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.getcwd()



# code_sentences = list()
# for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"PROCESSED_DATA")):
# 	index = 0
# 	for file in files:
# 		file_path = os.path.join(r,file)
# 		with open(file_path,"r") as f:
# 			data = f.read()
# 		sentence = data.split(" ")
		
# 		labeled_sentence = gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(str(data)),tags="tags_" + str(index))
# 		code_sentences.append(labeled_sentence)
# 		index = index + 1


# print "Building Doc2Vec model......."
# model = gensim.models.Doc2Vec(min_alpha=0.025,alpha=0.025,min_count=30,size=200,workers=6,window=5)

# model.build_vocab(code_sentences)

# for epoch in range(10):
# 	print "Epoch : " + str(epoch)
# 	model.train(code_sentences)
# 	model.alpha -=0.002
# 	model.min_alpha = model.alpha


# model.save("doc2vec")

# model.wv.save_word2vec_format("doc2vec.txt",fvocab=None,binary=False)

# Evaluation part --------------------------------------
model = gensim.models.Doc2Vec.load("doc2vec")

sentence_1 = "private void"
sentence_2 = "public void"

vec_1 = model.infer_vector(sentence_1.split(" "))
vec_2 = model.infer_vector(sentence_2.split(" "))
similarity = model.docvecs.similarity_unseen_docs(model,sentence_1.split(" "),sentence_2.split(" "))
print similarity