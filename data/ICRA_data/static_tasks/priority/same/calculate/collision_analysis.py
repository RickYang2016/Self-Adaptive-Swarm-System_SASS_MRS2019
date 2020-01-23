import matplotlib.pyplot as plt
from dateutil.parser import parse
import time
import numpy as np
import os

all_data = [[85, 101, 81, 78, 76, 54, 54, 75, 78, 57], \
			[78, 47, 82, 56, 81, 54, 58, 55, 81, 62], \
			[114, 146, 164, 115, 103, 179, 114, 134, 99, 147], \
			[153, 112, 132, 164, 131, 140, 113, 115, 118, 114]]

# draw the Per Task Negotiation Energy Cost graph
labels = ['T_Low_E', 'Low_E', 'T_High_E', 'High_E']

bplot = plt.boxplot(all_data, \
					patch_artist=True, \
					labels=labels, \
					boxprops = {'color':'black','facecolor':'#9999ff'}, \
					flierprops = {'marker':'o','markerfacecolor':'white','color':'black'}, \
					whiskerprops = {'color':'black', 'linestyle':'-'})

# plt.title('Per Task Negotiation Energy Cost', fontsize=20)

colors = ['pink', 'lightblue', 'lightgreen', 'lightyellow']
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

plt.tick_params(top='off', right='off')
# plt.grid(axis='y', which='major')
# plt.xlabel('Three separate samples')
plt.ylabel('Collision Frequency', fontsize=20)
plt.xticks(fontsize=20)
plt.show()
