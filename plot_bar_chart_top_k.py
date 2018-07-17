import numpy as np
import matplotlib.pyplot as plt
 
# data to plot




n_groups = 9
top_1 = (0.52, 0.37, 0.32, 0.42, 0.36, 0.30, 0.34, 0.36, 0.81)
top_5 = (0.58, 0.49, 0.51, 0.482, 0.512, 0.556, 0.442, 0.61, 0.82)
top_10 =(0.72, 0.78, 0.58, 0.52, 0.70, 0.63, 0.57, 0.66, 0.89)
# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
print index
bar_width = 0.2
opacity = 0.99
 
rects1 = plt.bar(index - bar_width, top_1, bar_width,
                 alpha=opacity,
                 color='b',
                 label='top-1',)


rects2 = plt.bar(index , top_5, bar_width,
                 alpha=opacity,
                 color='r',
                 label='top-5')
 

rects3 = plt.bar(index + bar_width, top_10, bar_width,
                 alpha=opacity,
                 color='g',
                 label='top-10')


plt.xlabel('Software Projects')
plt.ylabel('MAP Scores')
# plt.title('Scores by person')
plt.xticks(index - 0.04, ("antlr","zeromq","factual","fpml","lucene","mongodb","log4j","spring","datastax"))
plt.legend()
 
plt.tight_layout()
plt.show()