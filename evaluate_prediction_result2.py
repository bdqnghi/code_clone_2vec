import numpy as np
import scipy.stats as stats
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import os
import codecs
import csv
from sklearn.mixture import GMM
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
# This file is to draw distribution curve
from sklearn import svm
Y_raw = list()
X_raw = list()
y_predicted = list()
PROJECT = "antlr"

LABEL_ROW = 2
with codecs.open("./codelabel_result/bi2vec_" + PROJECT + "_10.csv","r") as f_csv:
	reader = csv.reader(f_csv)

	for i,row in enumerate(reader):
		if i == 0:
			continue
		if int(row[LABEL_ROW]) == 1 or int(row[LABEL_ROW]) == -1:
			if int(row[LABEL_ROW]) == 1:

				Y_raw.append(int(row[LABEL_ROW]))
			else:
				Y_raw.append(0)
			X_raw.append(float(row[6]))

print len(X_raw)
print len(Y_raw)
X = np.array(X_raw)
X = np.reshape(X,(-2,1))
Y = np.array(Y_raw)

print len(X)
print len(Y)
# print X

skf = StratifiedKFold(n_splits=10,random_state=40)
skf.get_n_splits(X,Y)

# X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3, random_state = 42)

index = 0

precision_score_list_LR = list()
recall_score_list_LR = list()
precision_score_list_SVC_poly = list()
recall_score_list_SVC_poly = list()
precision_score_list_RF = list()
recall_score_list_RF = list()
for train_index, test_index in skf.split(X,Y):
	print "########################"
	X_train, X_test = X[train_index], X[test_index]
	# X_train, X_test = X.iloc[train_index], X.iloc[test_index]
	Y_train, Y_test = Y[train_index], Y[test_index]

# X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size = 0.2,random_state = 45)
# X_train, X_test, y_train, y_test = X[train], X[test], y[train], y[test]

	clf_gmm = GMM(n_components=2,init_params="wc",n_iter=20,covariance_type="full")
	clf_gmm.means = np.array([X_train[Y_train == i].mean(axis=0) for i in range(2)])
	clf_gmm.fit(X_train)

	Y_predicted = clf_gmm.predict(X_test)

	print "GMM -------------"
	print precision_score(Y_test,Y_predicted,average="weighted")
	print recall_score(Y_test,Y_predicted,average="weighted")

	clf_lr_ = linear_model.LogisticRegression(C=1e5)
	clf_lr_.fit(X_train, Y_train)
	Y_predicted  = clf_lr_.predict(X_test);

	print "LR -------------"
	print precision_score(Y_test,Y_predicted,average="weighted")
	print recall_score(Y_test,Y_predicted,average="weighted")
	precision_score_list_LR.append(precision_score(Y_test,Y_predicted,average="weighted"))
	recall_score_list_LR.append(recall_score(Y_test,Y_predicted,average="weighted"))


	clf_random_forest = RandomForestClassifier(n_estimators=150, random_state=30).fit(X_train, Y_train)
	clf_random_forest.fit(X_train, Y_train)
	Y_predicted  = clf_random_forest.predict(X_test);

	print "RF ------------"
	print precision_score(Y_test,Y_predicted,average="weighted")
	print recall_score(Y_test,Y_predicted,average="weighted")
	precision_score_list_RF.append(precision_score(Y_test,Y_predicted,average="weighted"))
	recall_score_list_RF.append(recall_score(Y_test,Y_predicted,average="weighted"))


	clf_svc_linear = svm.SVC(kernel='linear', C=1)
	clf_svc_linear.fit(X_train,Y_train)
	Y_predicted  = clf_svc_linear.predict(X_test);

	print "SVC Linear ------------"
	print precision_score(Y_test,Y_predicted,average="weighted")
	print recall_score(Y_test,Y_predicted,average="weighted")

	clf_svc_linear = svm.SVC(kernel='poly', C=1)
	clf_svc_linear.fit(X_train,Y_train)
	Y_predicted  = clf_svc_linear.predict(X_test);

	print "SVC poly ---------------"
	print precision_score(Y_test,Y_predicted,average="weighted")
	print recall_score(Y_test,Y_predicted,average="weighted")
	precision_score_list_SVC_poly.append(precision_score(Y_test,Y_predicted,average="weighted"))
	recall_score_list_SVC_poly.append(recall_score(Y_test,Y_predicted,average="weighted"))


	clf_svc_linear = svm.SVC(kernel='rbf', C=1)
	clf_svc_linear.fit(X_train,Y_train)
	Y_predicted  = clf_svc_linear.predict(X_test);

	print "SVC rbf -------------"
	print precision_score(Y_test,Y_predicted,average="weighted")
	print recall_score(Y_test,Y_predicted,average="weighted")

print "---------------------------------------------------------------------------------------------------------"

print "LR all : " + str(np.mean(np.array(precision_score_list_LR))) + " , " +  str(np.mean(np.array(recall_score_list_LR)))

print "RF all : " + str(np.mean(np.array(precision_score_list_RF))) + " , " +  str(np.mean(np.array(recall_score_list_RF)))

print "SVC poly all : " + str(np.mean(np.array(precision_score_list_SVC_poly))) + " , " +  str(np.mean(np.array(recall_score_list_SVC_poly)))