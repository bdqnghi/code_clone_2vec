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
import sys
from sklearn.neighbors import NearestNeighbors

cs_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/cs_vectors_8.txt",binary=False)
java_vectors = KeyedVectors.load_word2vec_format("./bi2vec_vectors/java_vectors_8.txt",binary=False)

print java_vectors.similar_by_vector(cs_vectors[":"], topn=30)
# print cs_vectors.similar_by_vector(java_vectors["package"], topn=30)