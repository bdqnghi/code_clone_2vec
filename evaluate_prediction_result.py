import numpy as np
import scipy.stats as stats
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import gensim
import os
import codecs
import csv
from sklearn.mixture import GMM
# This file is to draw distribution curve

y_true = list()
y_predicted = list()
with codecs.open("./codelabel_result/bi2vec_spring_8.csv","r") as f_csv:
	reader = csv.reader(f_csv)

	for i,row in enumerate(reader):
		if i == 0:
			continue
		if int(row[2]) == 1 or int(row[2]) == -1:
			y_true.append(int(row[2]))

			predicted = -1
			print row[5]
			if float(row[5]) > 0.3:
				predicted = 1
			y_predicted.append(predicted)

# print len(y_true)
# np_y_true = np.array(y_true)
# print np_y_true
# np_y_predicted = np.array(y_predicted)
# print np_y_predicted
# print precision_score(np_y_true,np_y_predicted,average="weighted")
# print recall_score(np_y_true,np_y_predicted,average="weighted")

GMM = GMM(n_components=2,init_params="wc",n_iter=20)

