import matplotlib.pyplot as plt
import matplotlib
from dateutil.parser import parse
import time
import numpy as np
import os

path1 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/priority/same/calculate/m_t_l"
path2 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/priority/same/calculate/m_l"
path3 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/priority/same/calculate/m_t_h"
path4 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/priority/same/calculate/m_h"
path5 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/priority/same/calculate/runEnergyCost_l"
path6 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/priority/same/calculate/runEnergyCost_h"

files1 = os.listdir(path1)
files2 = os.listdir(path2)
files3 = os.listdir(path3)
files4 = os.listdir(path4)
files5 = os.listdir(path5)
files6 = os.listdir(path6)

energy_sum_no_negotiation,energy_sum_no_negotiation_l,energy_sum_no_negotiation_h,energy_sum_robots_t_l,energy_sum_robots_l,energy_sum_robots_t_h,energy_sum_robots_h = [],[],[],[],[],[],[]
energy_sum_robots_t_l_c,energy_sum_robots_l_c,energy_sum_robots_t_h_c,energy_sum_robots_h_c = [],[],[],[]
all_data = []
all_mean = []
all_comm = []

# w1 = open('/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/5_robots_energy_cost.txt', 'a')
# w2 = open('/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/10_robots_energy_cost.txt', 'a')
# w3 = open('/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/15_robots_energy_cost.txt', 'a')
# w4 = open('/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/20_robots_energy_cost.txt', 'a')

# no negotitation energy cost
# low energy
for file in files5:
	if not os.path.isdir(file):
		energy_sum = []
		f = open(path5 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			energy_sum.append(sum(value[1:]))

	energy_sum_no_negotiation_l.append(energy_sum[0] - energy_sum[-1])

# print("system no negotiation energy cost is " + str(energy_sum_no_negotiation))

# high energy
for file in files6:
	if not os.path.isdir(file):
		energy_sum = []
		f = open(path6 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			energy_sum.append(sum(value[1:]))

	energy_sum_no_negotiation_h.append(energy_sum[0] - energy_sum[-1])

# print("system no negotiation energy cost is " + str(energy_sum_no_negotiation))

# 5 robots negotiation energy cost
for file in files1:
	if not os.path.isdir(file):
		energy_sum = []
		f = open(path1 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			energy_sum.append(sum(value[1:]))

	energy_sum_robots_t_l.append(energy_sum[0] - energy_sum[-1])
	energy_sum_robots_t_l_c.append(energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation_l[0])
	# per_task_energy_cost_5robots.append(energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[0])

all_data.append(energy_sum_robots_t_l)
# all_data.append(per_task_energy_cost_5robots)
all_mean.append(np.mean(energy_sum_robots_t_l_c))
all_comm.append(energy_sum_robots_t_l_c)
energy_sum_no_negotiation.append(energy_sum_no_negotiation_l[0])

# print("one task 5 robots system's negotiation energy cost is " + str(energy_sum_5robots))
# print("one task 5 robots system's negotiation per task energy cost is " + str(per_task_energy_cost_5robots))

# 10 robots negotiation energy cost
for file in files2:
	if not os.path.isdir(file):
		energy_sum = []
		f = open(path2 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			energy_sum.append(sum(value[1:]))

	energy_sum_robots_l.append(energy_sum[0] - energy_sum[-1])
	energy_sum_robots_l_c.append(energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation_l[0])
	# per_task_energy_cost_10robots.append((energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[1]) / 2)

all_data.append(energy_sum_robots_l)
all_mean.append(np.mean(energy_sum_robots_l_c))
all_comm.append(energy_sum_robots_l_c)
energy_sum_no_negotiation.append(energy_sum_no_negotiation_l[0])

# print("two tasks 10 robots system's negotiation energy cost is " + str(energy_sum_10robots))
# print("two tasks 10 robots system's negotiation per task energy cost is " + str(per_task_energy_cost_10robots))

# 15 robots negotiation energy cost
for file in files3:
	if not os.path.isdir(file):
		energy_sum = []
		f = open(path3 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			energy_sum.append(sum(value[1:]))

	energy_sum_robots_t_h.append(energy_sum[0] - energy_sum[-1])
	energy_sum_robots_t_h_c.append(energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation_h[0])
	# per_task_energy_cost_15robots.append((energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[2]) / 3)

all_data.append(energy_sum_robots_t_h)
all_mean.append(np.mean(energy_sum_robots_t_h_c))
all_comm.append(energy_sum_robots_t_h_c)
energy_sum_no_negotiation.append(energy_sum_no_negotiation_h[0])

# print("three tasks 15 robots system's negotiation energy cost is " + str(energy_sum_15robots))
# print("three tasks 15 robots system's negotiation per task energy cost is " + str(per_task_energy_cost_15robots))

# 20 robots negotiation energy cost
for file in files4:
	if not os.path.isdir(file):
		energy_sum = []
		f = open(path4 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			energy_sum.append(sum(value[1:]))

	energy_sum_robots_h.append(energy_sum[0] - energy_sum[-1])
	energy_sum_robots_h_c.append(energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation_h[0])
	# per_task_energy_cost_20robots.append((energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[3]) / 4)

all_data.append(energy_sum_robots_h)
all_mean.append(np.mean(energy_sum_robots_h_c))
all_comm.append(energy_sum_robots_h_c)
energy_sum_no_negotiation.append(energy_sum_no_negotiation_h[0])

# print("four tasks 20 robots system's negotiation energy cost is " + str(energy_sum_20robots))
# print("three tasks 15 robots system's negotiation per task energy cost is " + str(per_task_energy_cost_20robots))


# print("all_mean is " + str(all_mean))

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
plt.ylabel('Energy Cost', fontsize=20)
plt.xticks(fontsize=20)
plt.show()


# draw the Per Task Negotiation Energy Cost graph
labels = ['T_Low_E', 'Low_E', 'T_High_E', 'High_E']

bplot = plt.boxplot(all_comm, \
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
plt.ylabel('Energy Cost', fontsize=20)
plt.xticks(fontsize=20)
plt.show()





# # draw the Energy Cost graph
# matplotlib.rcParams['font.sans-serif'] = ['SimHei']
# matplotlib.rcParams['axes.unicode_minus'] = False

# label_list = ['T_Low_E', 'Low_E', 'T_High_E', 'High_E']
# num_list1 = all_mean
# num_list2 = energy_sum_no_negotiation
# x = range(len(num_list1))
# rects1 = plt.bar(align="center", left=x, height=num_list1, width=0.3, alpha=0.8, color='lightblue', label="Communication Energy Cost")
# rects2 = plt.bar(align="center", left=x, height=num_list2, width=0.3, color='lightgreen', label="Moving Energy Cost", bottom=num_list1)
# plt.ylim(0, 1000)
# plt.ylabel('Energy Cost', fontsize=20)
# plt.xticks(x, label_list)
# # plt.xlabel("year")
# # plt.title("company")
# plt.legend()
# plt.show()
