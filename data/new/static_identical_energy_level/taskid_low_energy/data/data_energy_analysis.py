import matplotlib.pyplot as plt
from dateutil.parser import parse
import time
import numpy as np

filename = 'time_energy.txt'
time,energy,energy_sum = [],[],[]
with open(filename, 'r') as f:
	lines = f.readlines()
	for line in lines:
		value = [float(s) for s in line.split()]
		time.append(value[0])
		energy.append(value[1:])
		energy_sum.append(sum(value[1:])/10)

# print(time)
# print(energy)

for i in range(10):
	plt.plot(time,[k[i] for k in energy])
plt.xlabel('Time (s)')
plt.ylabel('Battery Level (%)')
plt.legend([('robot%d' % (i+1)) for i in range(10)])
plt.show()

plt.figure()
plt.plot(time,energy_sum)
plt.xlabel('Time (s)')
plt.ylabel('Battery Level (%)')
plt.legend(['System'])
plt.show()

z = []
x = []
for j in range(len(energy[0])):
	z.append([i[j] for i in energy])

	x.append(z[j][0] - z[j][-1])

print(x)
print(max(x)/time[-1])
print(min(x)/time[-1])
print(np.mean(x)/time[-1])