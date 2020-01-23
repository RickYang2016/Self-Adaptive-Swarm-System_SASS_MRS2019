import matplotlib.pyplot as plt
from dateutil.parser import parse
import time
import numpy as np
import os
import itertools as it
from datetime import datetime

path1 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/priority/task_low_energy_static/same/m3"
path2 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/priority/low_energy_static/same/m3"
path3 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/priority/task_high_energy_static/same/m3"
path4 = "/home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/priority/high_energy_static/same/m3"

# task_low_energy
files1 = os.listdir(path1)
time1 = []

for file1 in files1:
	if not os.path.isdir(file1):
		step1, tmpTime1, energy_sum1 = [],[],[]
		f1 = open(path1 + "/" + file1, "r");

		for line in f1:
			value1 = [str(s) for s in line.split()]
			step1.append(value1[0])
			tmpTime1.append(value1[1])
			# energy_sum1.append(sum(list(map(float ,value1[2:]))))
			energy_sum1.append(sum(list(map(float, value1[2:])))/20)
			time1.append((datetime.strptime(value1[1], "%M:%S.%f") - datetime.strptime(tmpTime1[0], "%M:%S.%f")).seconds + \
						 ((datetime.strptime(value1[1], "%M:%S.%f") - datetime.strptime(tmpTime1[0], "%M:%S.%f")).microseconds / 1000000))
			# time1.append((datetime.strptime(value1[1], "%M:%S.%f") - datetime.strptime(tmpTime1[0], "%M:%S.%f")).seconds)

# low_energy
files2 = os.listdir(path2)
time2 = []

for file2 in files2:
	if not os.path.isdir(file2):
		step2, tmpTime2, energy_sum2 = [],[],[]
		f2 = open(path1 + "/" + file2, "r");

		for line2 in f2:
			value2 = [str(s) for s in line2.split()]
			step2.append(value2[0])
			tmpTime2.append(value2[1])
			# energy_sum2.append(sum(list(map(float ,value2[2:]))))
			energy_sum2.append(sum(list(map(float, value2[2:])))/20)
			time2.append((datetime.strptime(value2[1], "%M:%S.%f") - datetime.strptime(tmpTime2[0], "%M:%S.%f")).seconds + \
						 ((datetime.strptime(value2[1], "%M:%S.%f") - datetime.strptime(tmpTime2[0], "%M:%S.%f")).microseconds / 1000000))
			# time2.append((datetime.strptime(value2[1], "%M:%S.%f") - datetime.strptime(tmpTime2[0], "%M:%S.%f")).seconds)
# print(energy_sum2)
# print(time2)

# task_high_energy
files3 = os.listdir(path3)
time3 = []

for file3 in files3:
	if not os.path.isdir(file3):
		step3, tmpTime3, energy_sum3 = [],[],[]
		f3 = open(path3 + "/" + file3, "r");

		for line3 in f3:
			value3 = [str(s) for s in line3.split()]
			step3.append(value3[0])
			tmpTime3.append(value3[1])
			# energy_sum3.append(sum(list(map(float ,value3[2:]))))
			energy_sum3.append(sum(list(map(float ,value3[2:])))/20)
			time3.append((datetime.strptime(value3[1], "%M:%S.%f") - datetime.strptime(tmpTime3[0], "%M:%S.%f")).seconds + \
						 ((datetime.strptime(value3[1], "%M:%S.%f") - datetime.strptime(tmpTime3[0], "%M:%S.%f")).microseconds / 1000000))
			# time3.append((datetime.strptime(value3[1], "%M:%S.%f") - datetime.strptime(tmpTime3[0], "%M:%S.%f")).seconds)

# high_energy
files4 = os.listdir(path4)
time4 = []

for file4 in files4:
	if not os.path.isdir(file4):
		step4, tmpTime4, energy_sum4 = [],[],[]
		f4 = open(path4 + "/" + file4, "r");

		for line4 in f4:
			value4 = [str(s) for s in line4.split()]
			step4.append(value4[0])
			tmpTime4.append(value4[1])
			# energy_sum4.append(sum(list(map(float ,value4[2:]))))
			energy_sum4.append(sum(list(map(float ,value4[2:])))/20)
			time4.append((datetime.strptime(value4[1], "%M:%S.%f") - datetime.strptime(tmpTime4[0], "%M:%S.%f")).seconds + \
						 ((datetime.strptime(value4[1], "%M:%S.%f") - datetime.strptime(tmpTime4[0], "%M:%S.%f")).microseconds / 1000000))
			# time4.append((datetime.strptime(value4[1], "%M:%S.%f") - datetime.strptime(tmpTime4[0], "%M:%S.%f")).seconds)

plt.figure()
plt.plot(time1,energy_sum1)
# plt.plot(time2,energy_sum2)
plt.plot(time3,energy_sum3)
plt.plot(time4,energy_sum4)
plt.xlabel('Time (s)')
plt.ylabel('Battery Level (%)')
plt.legend(['task_low_energy','low_energy','task_high_energy', 'high_energy'])
plt.show()
