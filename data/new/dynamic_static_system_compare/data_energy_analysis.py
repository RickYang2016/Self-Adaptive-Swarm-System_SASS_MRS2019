import matplotlib.pyplot as plt
from dateutil.parser import parse
import time
import numpy as np
import os
import itertools as it

path1 = "/home/rick/SRSS/data/new/dynamic/1+1+1/modify/all_energy_level"
path2 = "/home/rick/SRSS/data/new/dynamic/2+1/modify/all_energy_level"
path3 = "/home/rick/SRSS/data/new/dynamic/1+2/modify/all_energy_level"

#id
files1 = os.listdir(path1)
energy_sum_sum1,energy_sum_mean1,energy_sum_sum_mean1,time_mean1 = [],[],[],[]

for file in files1:
	if not os.path.isdir(file):
		time,energy,energy_sum,z,x = [],[],[],[],[]
		f = open(path1 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			time.append(value[0])
			energy.append(value[1:])
			energy_sum.append(sum(value[1:])/20)

		energy_sum_sum1.append(energy_sum)

min_len1 = min((len(i) for i in energy_sum_sum1))
print(min_len1)

for i in energy_sum_sum1:
	energy_sum_mean1.append(i[0:min_len1])

energy_sum_sum_mean1 = [sum(x)/10 for x in it.zip_longest(*energy_sum_mean1, fillvalue = 0)]
print(energy_sum_sum_mean1, len(energy_sum_sum_mean1))

for i in range(len(energy_sum_sum_mean1)):
	time_mean1.append(i)

#high
files2 = os.listdir(path2)
energy_sum_sum2,energy_sum_mean2,energy_sum_sum_mean2,time_mean2 = [],[],[],[]

for file in files2:
	if not os.path.isdir(file):
		time,energy,energy_sum,z,x = [],[],[],[],[]
		f = open(path2 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			time.append(value[0])
			energy.append(value[1:])
			energy_sum.append(sum(value[1:])/20)

		energy_sum_sum2.append(energy_sum)

min_len2 = min((len(i) for i in energy_sum_sum2))
print(min_len2)

for i in energy_sum_sum2:
	energy_sum_mean2.append(i[0:min_len2])

energy_sum_sum_mean2 = [sum(x)/10 for x in it.zip_longest(*energy_sum_mean2, fillvalue = 0)]
print(energy_sum_sum_mean2, len(energy_sum_sum_mean2))

for i in range(len(energy_sum_sum_mean2)):
	time_mean2.append(i)

#low
files3 = os.listdir(path3)
energy_sum_sum3,energy_sum_mean3,energy_sum_sum_mean3,time_mean3 = [],[],[],[]

for file in files3:
	if not os.path.isdir(file):
		time,energy,energy_sum,z,x = [],[],[],[],[]
		f = open(path3 + "/" + file, "r");
		for line in f:
			value = [float(s) for s in line.split()]
			time.append(value[0])
			energy.append(value[1:])
			energy_sum.append(sum(value[1:])/20)

		energy_sum_sum3.append(energy_sum)

min_len3 = min((len(i) for i in energy_sum_sum3))
print(min_len3)

for i in energy_sum_sum3:
	energy_sum_mean3.append(i[0:min_len3])

energy_sum_sum_mean3 = [sum(x)/10 for x in it.zip_longest(*energy_sum_mean3, fillvalue = 0)]
print(energy_sum_sum_mean3, len(energy_sum_sum_mean3))

for i in range(len(energy_sum_sum_mean3)):
	time_mean3.append(i)


plt.figure()
plt.plot(time_mean1,energy_sum_sum_mean1)
plt.plot(time_mean2,energy_sum_sum_mean2)
plt.plot(time_mean3,energy_sum_sum_mean3)
plt.xlabel('Time (s)')
plt.ylabel('Battery Level (%)')
plt.legend(['1+1+1_System_Energy','2+1_System_Energy','1+2_System_Energy'])
plt.show()
