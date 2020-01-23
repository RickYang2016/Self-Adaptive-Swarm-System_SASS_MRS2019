import matplotlib.pyplot as plt
from dateutil.parser import parse
import time
import numpy as np
import os

path = "/home/rick/SRSS/data/new/static_identical_energy_level/id/all_distance"
files = os.listdir(path)
distance_sum_sum,distance_sum_mean,total_distance = [],[],[]

w = open('/home/rick/SRSS/data/new/static_identical_energy_level/id/id_distance.txt', 'a')

for file in files:
	if not os.path.isdir(file):
		time,distance,distance_sum,z,x = [],[],[],[],[]
		f = open(path + "/" + file, "r");
		# iter_f = iter(f)
		for line in f:
			value = [float(s) for s in line.split()]
			time.append(value[0])
			distance.append(value[1:])
			distance_sum.append(sum(value[1:]))
		# print(distance_sum, len(distance_sum))

		# distance_sum_sum = np.sum([distance_sum_sum,distance_sum], axis = 0)

		# distance_sum_sum.append(distance_sum)

		# #individual distance plot
		# plt.figure()
		# plt.plot(time,distance_sum)
		# plt.xlabel('Time (s)')
		# plt.ylabel('distance (%)')
		# plt.legend(['System'])
		# plt.show()

# 		#energy_sum = []
		# calculate the min, max and mean
		for j in range(len(distance[0])):
			z.append([i[j] for i in distance])
			x.append(z[j][-1] - z[j][0])

		total_distance.append(sum(x))

		w.write("************experiment result****************" + '\n')
		w.write("max distance: " + str(max(x)) + '\n')
		w.write("min distance level: " + str(min(x)) + '\n')
		w.write("mean distance level: " + str(np.mean(x)) + '\n')
		w.write("*********************************************\n")

		# print(x)
		# print(sum(x))
		# print("max distance: ", max(x))
		# print("min distance: ", min(x))
		# print("mean distance: ", np.mean(x))
		# print("=========================================")
		# # print(energy_sum)

w.write("======================================================================" + '\n')
w.write("======================================================================" + '\n')
w.write("experiments system distance: " + str(total_distance) + '\n')
w.write("======================================================================" + '\n')
w.write("======================================================================" + '\n')

print(total_distance)





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
# time,distance,energy_sum,energy_sum_sum = [],[],[],[]
# with open(filename, 'r') as f:
# 	lines = f.readlines()
# 	for line in lines:
# 		value = [float(s) for s in line.split()]
# 		time.append(value[0])
# 		distance.append(value[1:])
# 		energy_sum.append(sum(value[1:])/20)

# print(time)
# print(distance)

# for i in range(20):
# 	plt.plot(time,[k[i] for k in distance])
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
# for j in range(len(distance[0])):
# 	z.append([i[j] for i in distance])

# 	x.append(z[j][0] - z[j][-1])

# print(x)
# print(max(x)/time[-1])
# print(min(x)/time[-1])
# print(np.mean(x)/time[-1])
# print(energy_sum)





# filename = 'time_energy.txt'
# time,distance,energy_sum,energy_sum_sum = [],[],[],[]
# with open(filename, 'r') as f:
# 	lines = f.readlines()
# 	for line in lines:
# 		value = [float(s) for s in line.split()]
# 		time.append(value[0])
# 		distance.append(value[1:])
# 		energy_sum.append(sum(value[1:])/20)

# print(time)
# print(distance)

# for i in range(20):
# 	plt.plot(time,[k[i] for k in distance])
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

