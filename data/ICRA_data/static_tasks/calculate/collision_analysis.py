import matplotlib.pyplot as plt
from dateutil.parser import parse
import time
import numpy as np
import os

all_data = [[0, 10, 4, 0, 0, 6, 0, 1, 15, 1], \
			[8, 12, 11, 9, 18, 12, 15, 13, 13, 35], \
			[30, 66, 75, 80, 52, 66, 34, 75, 32, 81], \
			[135, 122, 93, 93, 76, 99, 159, 123, 65, 58]]

# draw the Per Task Negotiation Energy Cost graph
labels = ['R5+T1', 'R10+T2', 'R15+T3', 'R20+T4']

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
