import matplotlib.pyplot as plt
from dateutil.parser import parse
import time
import numpy as np
import os

path = "/home/rick/SRSS/data/new/static_identical_energy_level/high_energy/all_energy_level"
files = os.listdir(path)
energy_sum_sum,energy_sum_mean,total_energy,total_energy1,total_energy2 = [],[],[],[],[]

w = open('/home/rick/SRSS/data/new/static_identical_energy_level/high_energy/high_energy_energy.txt', 'a')

for file in files:
	if not os.path.isdir(file):
		time,energy,energy_sum,z,x = [],[],[],[],[]
		f = open(path + "/" + file, "r");
		# iter_f = iter(f)
		for line in f:
			value = [float(s) for s in line.split()]
			time.append(value[0])
			energy.append(value[1:])
			energy_sum.append(sum(value[1:])/20)
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

		# calculate the min, max and mean
		for j in range(len(energy[0])):
			z.append([i[j] for i in energy])
			x.append(z[j][0] - z[j][-1])

		total_energy.append(sum(x))
		total_energy1.append(sum(x)/20)
		total_energy2.append(sum(x)/20/time[-1])


		w.write("============experiment result================" + '\n')
		w.write("max battery level cost: " + str(max(x)) + '\n')
		w.write("min battery level cost: " + str(min(x)) + '\n')
		w.write("mean battery level cost: " + str(np.mean(x)) + '\n')
		w.write("*********************************************" + '\n')
		w.write("max battery level cost/per second: " + str(max(x)/time[-1]) + '\n')
		w.write("min battery level cost/per second: " + str(min(x)/time[-1]) + '\n')
		w.write("mean battery level cost/per second: " + str(np.mean(x)/time[-1]) + '\n')

# 		# # print(x)
# 		# # print(sum(x))

		print("max battery level cost: ", max(x))
		print("min battery level cost: ", min(x))
		print("mean battery level cost: ", np.mean(x))
		print("=========================================")

		print("max battery level cost/per second: ", max(x)/time[-1])
		print("min battery level cost/per second: ", min(x)/time[-1])
		print("mean battery level cost/per second: ", np.mean(x)/time[-1])
		print("=========================================")

		# print(energy_sum)
w.write("======================================================================" + '\n')
w.write("experiments average system total energy cost: " + str(total_energy) + '\n')
w.write("*********************************************" + '\n')
w.write("experiments average system mean energy cost: " + str(total_energy1) + '\n')
w.write("*********************************************" + '\n')
w.write("experiments system energy cost/per second: " + str(total_energy2) + '\n')
w.write("*********************************************" + '\n')

print("experiments average system total energy cost: ", total_energy)
print("*********************************************")
print("experiments average system mean energy cost: ", total_energy1)
print("*********************************************")
print("experiments system energy mean cost/per second: ", total_energy2)


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

