import gensim
import os
import codecs
from sklearn.manifold import TSNE
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
import csv
from sklearn.metrics.pairwise import cosine_similarity

import sys


print "Loading word embedding..........."
cs_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/cs_vectors_new.txt",binary=False)
java_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/java_vectors_new.txt",binary=False)

print "Finish loading.............."
print cs_vectors.similar_by_vector(java_vectors["java.lang.Float.floatToIntBits(float)"], topn=10)
# print java_vectors.similar_by_vector(cs_vectors["java.util.ArrayList"], topn=30)

