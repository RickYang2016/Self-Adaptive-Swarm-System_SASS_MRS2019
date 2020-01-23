import matplotlib.pyplot as plt
import matplotlib
from dateutil.parser import parse
import time
import numpy as np
import os

path1 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/m5"
path2 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/m10"
path3 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/m15"
path4 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/m20"
path5 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/runEnergyCost"

files1 = os.listdir(path1)
files2 = os.listdir(path2)
files3 = os.listdir(path3)
files4 = os.listdir(path4)
files5 = os.listdir(path5)

energy_sum_no_negotiation,energy_sum_5robots,energy_sum_10robots,energy_sum_15robots,energy_sum_20robots = [],[],[],[],[]
per_task_energy_cost_5robots,per_task_energy_cost_10robots,per_task_energy_cost_15robots,per_task_energy_cost_20robots = [],[],[],[]
all_data = []
all_mean = []

w1 = open('/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/5_robots_energy_cost.txt', 'a')
w2 = open('/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/10_robots_energy_cost.txt', 'a')
w3 = open('/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/15_robots_energy_cost.txt', 'a')
w4 = open('/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/calculate/20_robots_energy_cost.txt', 'a')

# no negotitation energy cost
for file in files5:
	if not os.path.isdir(file):
		energy_sum = []
		f = open(path5 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			energy_sum.append(sum(value[1:]))

	energy_sum_no_negotiation.append(energy_sum[0] - energy_sum[-1])

energy_sum_no_negotiation.sort()

print("system no negotiation energy cost is " + str(energy_sum_no_negotiation))

# 5 robots negotiation energy cost
for file in files1:
	if not os.path.isdir(file):
		energy_sum = []
		f = open(path1 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			energy_sum.append(sum(value[1:]))

	energy_sum_5robots.append(energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[0])
	per_task_energy_cost_5robots.append(energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[0])

all_data.append(per_task_energy_cost_5robots)
all_mean.append(np.mean(energy_sum_5robots))

print("one task 5 robots system's negotiation energy cost is " + str(energy_sum_5robots))
# print("one task 5 robots system's negotiation per task energy cost is " + str(per_task_energy_cost_5robots))

# 10 robots negotiation energy cost
for file in files2:
	if not os.path.isdir(file):
		energy_sum = []
		f = open(path2 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			energy_sum.append(sum(value[1:]))

	energy_sum_10robots.append(energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[1])
	per_task_energy_cost_10robots.append((energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[1]) / 2)

all_data.append(per_task_energy_cost_10robots)
all_mean.append(np.mean(energy_sum_10robots))

print("two tasks 10 robots system's negotiation energy cost is " + str(energy_sum_10robots))
# print("two tasks 10 robots system's negotiation per task energy cost is " + str(per_task_energy_cost_10robots))

# 15 robots negotiation energy cost
for file in files3:
	if not os.path.isdir(file):
		energy_sum = []
		f = open(path3 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			energy_sum.append(sum(value[1:]))

	energy_sum_15robots.append(energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[2])
	per_task_energy_cost_15robots.append((energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[2]) / 3)

all_data.append(per_task_energy_cost_15robots)
all_mean.append(np.mean(energy_sum_15robots))

print("three tasks 15 robots system's negotiation energy cost is " + str(energy_sum_15robots))
# print("three tasks 15 robots system's negotiation per task energy cost is " + str(per_task_energy_cost_15robots))

# 20 robots negotiation energy cost
for file in files4:
	if not os.path.isdir(file):
		energy_sum = []
		f = open(path4 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			energy_sum.append(sum(value[1:]))

	energy_sum_20robots.append(energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[3])
	per_task_energy_cost_20robots.append((energy_sum[0] - energy_sum[-1] - energy_sum_no_negotiation[3]) / 4)

all_data.append(per_task_energy_cost_20robots)
all_mean.append(np.mean(energy_sum_20robots))

print("four tasks 20 robots system's negotiation energy cost is " + str(energy_sum_20robots))
# print("three tasks 15 robots system's negotiation per task energy cost is " + str(per_task_energy_cost_20robots))


print("all_mean is " + str(all_mean))

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
plt.ylabel('Energy Cost', fontsize=20)
plt.xticks(fontsize=20)
plt.show()

# draw the Energy Cost graph
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

label_list = ['R5+T1', 'R10+T2', 'R15+T3', 'R20+T4']
num_list1 = all_mean
num_list2 = energy_sum_no_negotiation
x = range(len(num_list1))
rects1 = plt.bar(align="center", left=x, height=num_list1, width=0.3, alpha=0.8, color='lightblue', label="Communication Energy Cost")
rects2 = plt.bar(align="center", left=x, height=num_list2, width=0.3, color='lightgreen', label="Moving Energy Cost", bottom=num_list1)
plt.ylim(0, 800)
plt.ylabel('Energy Cost', fontsize=20)
plt.xticks(x, label_list, fontsize=20)
# plt.xlabel("year")
# plt.title("company")
plt.legend()
plt.show()



# for file in files1:
# 	if not os.path.isdir(file):
# 		energy_sum_5robots = []
# 		# time,energy,energy_sum,z,x = [],[],[],[],[]
# 		f = open(path1 + "/" + file, "r");
# 		# iter_f = iter(f)
# 		for line in f:
# 			value = [float(s) for s in line.split()]
# 			# time.append(value[0])
# 			# energy.append(value[1:])
# 			energy_sum_5robots.append(sum(value[1:]))
		# print(energy_sum, len(energy_sum))

		# energy_sum_sum = np.sum([energy_sum_sum,energy_sum], axis = 0)

		# energy_sum_sum.append(energy_sum)

		# plt.figure()
		# # plt.plot(time,energy_sum)
		# plt.xlabel('Time (s)')
		# plt.ylabel('Battery Level (%)')
		# plt.legend(['System'])
		# plt.show()

		#energy_sum = []

		# # calculate the min, max and mean
		# for j in range(len(energy[0])):
		# 	z.append([i[j] for i in energy])
		# 	x.append(z[j][0] - z[j][-1])

		# total_energy.append(sum(x))
		# total_energy1.append(sum(x)/20)
		# total_energy2.append(sum(x)/20/time[-1])


		# w.write("============experiment result================" + '\n')
		# w.write("max battery level cost: " + str(max(x)) + '\n')
		# w.write("min battery level cost: " + str(min(x)) + '\n')
		# w.write("mean battery level cost: " + str(np.mean(x)) + '\n')
		# w.write("*********************************************" + '\n')
		# w.write("max battery level cost/per second: " + str(max(x)/time[-1]) + '\n')
		# w.write("min battery level cost/per second: " + str(min(x)/time[-1]) + '\n')
		# w.write("mean battery level cost/per second: " + str(np.mean(x)/time[-1]) + '\n')

		# # print(x)
		# # print(sum(x))

	# print("one task system negotiation energy cost is " + str(energy_sum[0] - energy_sum[-1] - 94.22))

		# print("max battery level cost: ", max(x))
		# print("min battery level cost: ", min(x))
		# print("mean battery level cost: ", np.mean(x))
		# print("=========================================")

		# print("max battery level cost/per second: ", max(x)/time[-1])
		# print("min battery level cost/per second: ", min(x)/time[-1])
		# print("mean battery level cost/per second: ", np.mean(x)/time[-1])
		# print("=========================================")

# 		# print(energy_sum)
# w.write("======================================================================" + '\n')
# w.write("experiments average system total energy cost: " + str(total_energy) + '\n')
# w.write("*********************************************" + '\n')
# w.write("experiments average system mean energy cost: " + str(total_energy1) + '\n')
# w.write("*********************************************" + '\n')
# w.write("experiments system energy cost/per second: " + str(total_energy2) + '\n')
# w.write("*********************************************" + '\n')

# print("experiments average system total energy cost: ", total_energy)
# print("*********************************************")
# print("experiments average system mean energy cost: ", total_energy1)
# print("*********************************************")
# print("experiments system energy mean cost/per second: ", total_energy2)


# print(energy_sum_sum, len(energy_sum_sum))

# for i in energy_sum_sum:
# 	energy_sum_mean.append(sum(energy_sum_sum[i][1:])/20)

# energy_sum_mean = np.sum(energy_sum_sum, axis=0)

# print(energy_sum_mean, len(energy_sum_mean))

# plt.figure()
# plt.plot(time,energy_sum_mean)
# plt.xlabel('Time (s)')
# plt.ylabel('Battery Level (%)')
# plt.legend(['System'])
# plt.show()

# filename = 'time_energy.txt'
# time,energy,energy_sum,energy_sum_sum = [],[],[],[]
# with open(filename, 'r') as f:
# 	lines = f.readlines()
# 	for line in lines:
# 		value = [float(s) for s in line.split()]
# 		time.append(value[0])
# 		energy.append(value[1:])
# 		energy_sum.append(sum(value[1:])/20)

# print(time)
# print(energy)

# for i in range(20):
# 	plt.plot(time,[k[i] for k in energy])
# plt.xlabel('Time (s)')
# plt.ylabel('Battery Level (%)')
# plt.legend([('robot%d' % (i+1)) for i in range(20)])
# plt.show()

# plt.figure()
# plt.plot(time,energy_sum)
# plt.xlabel('Time (s)')
# plt.ylabel('Battery Level (%)')
# plt.legend(['System'])
# plt.show()

# z = []
# x = []
# for j in range(len(energy[0])):
# 	z.append([i[j] for i in energy])

# 	x.append(z[j][0] - z[j][-1])

# print(x)
# print(max(x)/time[-1])
# print(min(x)/time[-1])
# print(np.mean(x)/time[-1])
# print(energy_sum)





# filename = 'time_energy.txt'
# time,energy,energy_sum,energy_sum_sum = [],[],[],[]
# with open(filename, 'r') as f:
# 	lines = f.readlines()
# 	for line in lines:
# 		value = [float(s) for s in line.split()]
# 		time.append(value[0])
# 		energy.append(value[1:])
# 		energy_sum.append(sum(value[1:])/20)

# print(time)
# print(energy)

# for i in range(20):
# 	plt.plot(time,[k[i] for k in energy])
# plt.xlabel('Time (s)')
# plt.ylabel('Battery Level (%)')
# plt.legend([('robot%d' % (i+1)) for i in range(20)])
# plt.show()

# plt.figure()
# plt.plot(time,energy_sum)
# plt.xlabel('Time (s)')
# plt.ylabel('Battery Level (%)')
# plt.legend(['System'])
# plt.show()

