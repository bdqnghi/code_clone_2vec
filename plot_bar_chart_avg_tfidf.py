import numpy as np
import matplotlib.pyplot as plt
 
# data to plot




n_groups = 9
means_avg = 	  (0.41, 0.57, 0.32, 0.44, 0.36, 0.41, 0.39, 0.60, 0.881)
means_avg_tfidf = (0.72, 0.78, 0.58, 0.52, 0.70, 0.63, 0.57, 0.66, 0.89)
 
# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
 
rects1 = plt.bar(index, means_avg, bar_width,
                 alpha=opacity,
                 color='b',
                 label='avg',)


rects2 = plt.bar(index + bar_width, means_avg_tfidf, bar_width,
                 alpha=opacity,
                 color='r',
                 label='avg-tfidf')
 
plt.xlabel('Projects')
plt.ylabel('MAP Scores')
# plt.title('Scores by person')
plt.xticks(index + 0.18, ("antlr","zeromq","factual","fpml","lucene","mongodb","log4j","spring","datastax"))
plt.legend()
 
plt.tight_layout()
plt.show()



# n_groups = 18
# means_avg = 	  (0.41, 0.37, 0.57, 0.56, 0.32, 0.40, 0.44, 0.40, 0.36, 0.29, 0.41, 0.51, 0.39, 0.563, 0.60, 0.59, 0.881, 0.76)
# means_avg_tfidf = (0.72, 0.54, 0.78, 0.73, 0.58, 0.57, 0.52, 0.48, 0.70, 0.59, 0.63, 0.58, 0.57, 0.569, 0.66, 0.61, 0.89,  0.82)
 
# # create plot
# fig, ax = plt.subplots()
# index = np.arange(n_groups)
# bar_width = 0.35
# opacity = 0.8
 
# rects1 = plt.bar(index, means_avg, bar_width,
#                  alpha=opacity,
#                  color='b',
#                  label='avg')
 
# rects2 = plt.bar(index + bar_width, means_avg_tfidf, bar_width,
#                  alpha=opacity,
#                  color='g',
#                  label='avg-tfidf')
 
# plt.xlabel('Projects')
# plt.ylabel('Scores')
# plt.title('Scores by person')
# plt.xticks(index + bar_width, ("antlr\nC#->Java","antlr\nJava->C#","zeromq\nC#->Java","zeromq\nJava->C#","factual\nC#->Java","factual\nJava->C#","fpml\nC#->Java","fpml\nJava->C#","lucene\nC#->Java","lucene\nJava->C#","mongodb\nC#->Java","mongodb\nJava->C#","log4j\nC#->Java","log4j\nJava->C#","spring\nC#->Java","spring\nJava->C#","datastax\nC#->Java","datastax\nJava->C#"))
# plt.legend()
 
# plt.tight_layout()
# plt.show()
