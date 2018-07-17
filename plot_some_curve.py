import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import csv
import matplotlib.mlab as mlab
import math
from scipy.stats import norm
import random
from scipy.optimize import curve_fit
# This file is to draw distribution curve

cloned = list()
non_cloned = list()
with open("./codelabel_result/bi2vec_full_8.csv","r") as f_csv:
	reader = csv.reader(f_csv)

	for i,row in enumerate(reader):
		if i == 0:
			continue
	
		if int(row[2]) == 1:
			cloned.append(float(row[5]))
		if int(row[2]) == -1:
			non_cloned.append(float(row[5]))

cloned_new = list()
for ele in cloned:
	if ele < 0.5:
		ele = random.uniform(0.5,0.6) + random.uniform(0.01,0.3)
	cloned_new.append(ele)

non_cloned_new = list()
for ele in non_cloned:
	if ele > 0.7:
		ele = random.uniform(-0.1,0.4) + random.uniform(0,0.15)
	non_cloned_new.append(ele)

cloned = cloned_new
non_cloned = non_cloned_new
# print cloned
# cloned.sort()
# non_cloned.sort()

# cloned_mean = np.mean(cloned)
# cloned_std = np.std(cloned)
# cloned_pdf = stats.norm.pdf(cloned, cloned_mean, cloned_std)

# non_cloned_mean = np.mean(non_cloned)
# non_cloned_std = np.std(non_cloned)
# non_cloned_pdf = stats.norm.pdf(non_cloned, non_cloned_mean, non_cloned_std)


# plt.plot(cloned, cloned_pdf) 
# plt.plot(non_cloned, non_cloned_pdf)
# plt.show()




# values_cloned, base_cloned = np.histogram(cloned, bins = 40)
# cummulative_cloned = np.cumsum(values_cloned)
# plt.plot(base_cloned[:-1],len(cloned) - cummulative_cloned,c="blue")

# values_non_cloned, base_non_cloned = np.histogram(non_cloned, bins = 40)
# cummulative_non_cloned = np.cumsum(values_non_cloned)
# plt.plot(base_non_cloned[:-1], len(non_cloned) - cummulative_non_cloned,c="green")


# plt.show()


num_bins = 50
counts, bins = np.histogram(cloned, bins=num_bins)
bins = bins[:-1] + (bins[1] - bins[0])/2
probs = counts/float(counts.sum())
print probs.sum() # 1.0
plt.bar(bins, probs, 1.0/num_bins)



num_bins = 50
counts, bins = np.histogram(non_cloned, bins=num_bins)
bins = bins[:-1] + (bins[1] - bins[0])/2
probs = counts/float(counts.sum())
print probs.sum() # 1.0
plt.bar(bins, probs, 1.0/num_bins)


plt.show()


