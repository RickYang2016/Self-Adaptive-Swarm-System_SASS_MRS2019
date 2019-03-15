#!/usr/bin/env python3

#Author: Zhiwei Luo

from task import Strategy, NetworkInterface
from COREDebugger import COREDebuggerVirtual
import time
import os
import math
import sys
import socket

class Strategy_SRSS(Strategy):
	network = None
	controlNet = None

	local_id = 0
	local_task_id = 0
	local_task_duration = 0
	local_energy_level = 100
	local_direction = [1, 0]			# Direction vector: not necessary to be normalized
	local_coordinate = [0, 0]
	local_step_size = 1
	local_go_interval = 0.5
	local_round = 0
	local_stage = 'start'
	local_step = 0
	local_negotiation = 1
	local_queue = []					# [3, 1, 2] means the priority: robot-3 > robot-1 > robot-2	
	local_negotiation_result = False	# If all the queues are the same, set as True, otherwise, False
	send_data_history = None

	global_num_robots = 1
	global_num_tasks = 2
	global_min_require_robots = 1
	global_group_num_robots = 1
	global_energy_level = {}			# {1: 100, 2: 99, 3: 85, ...}
	global_negotiation_queue = {}		# {'1': [3, 1, 2], '2': [3, 2, 1], '3': [3, 1, 2], ...}
	global_agreement = {}				# {'1': True, '2': False, '3': True, ...}

	local_debugger = None

	def __init__(self, id, \
				coordinate=[50, 50], \
				direction=[1, 1], \
				step_size=1, \
				go_interval=0.5, \
				num_robots=1, \
				controlNet='172.16.0.254'):
		self.local_id = id
		self.local_coordinate = coordinate
		self.local_direction = direction
		self.local_step_size = step_size
		self.local_go_interval = go_interval
		self.global_num_robots = num_robots
		self.controlNet = controlNet
		self.network = NetworkInterface(port=19999)
		self.network.initSocket()
		self.network.startReceiveThread()
		# Debugger tool:
		self.local_debugger = COREDebuggerVirtual((controlNet, 12888))

	def checkFinished(self):
		return False

	def go(self):
		if self.local_stage == 'start':
			self.local_round = self.local_round + 1
			self.local_stage = 'selection'
			self.selection()
		elif self.local_stage == 'selection':
			self.local_stage = 'formation'
			self.formation()
		elif self.local_stage == 'formation':
			self.local_stage = 'routing'
			self.routing()
		elif self.local_stage == 'routing':
			self.local_stage = 'end'
		elif self.local_stage == 'end':
			self.walk_one_step()
			# default stage is 'end'
			# if new tasks are released: local_stage -> 'start'
		else:
			print('Unknown state.')
		time.sleep(self.local_go_interval)

	def global_condition_func(self, recv_data):
		# TODO: 
		# 	Check if there is a task released.
		# 	Set self.local_stage -> 'start'
		# 	If some task is executing, put it into a place to store
		pass

	def message_communication(self, send_data, condition_func, time_out=10):
		# input: send_data is a dictionary
		# output: recv_data is also a dictionary
		# new task release: trigger a new round of <selection-formation-routing>
		while True:
			time_start = time.time()
			self.network.sendStringData(send_data)
			# self.local_debugger.send_to_monitor('send: ' + str(send_data))
			while time.time() - time_start < time_out:
				try:
					recv_data = self.network.retrieveData()
					if recv_data != None:
						# self.local_debugger.send_to_monitor('recv: ' + str(recv_data))
						# if new task is released
						self.global_condition_func(recv_data)
						if condition_func(recv_data) == True:
							self.send_data_history = send_data
							return recv_data
						else:
							continue
					else:
						continue
				except Exception as e:
					raise e
			self.network.sendStringData(self.send_data_history)
				
	def get_basic_status(self):
		status_dict = { \
						'id': self.local_id,
						'round': self.local_round,
						'stage': self.local_stage
						}
		return status_dict

	def selection(self):
		self.selection_step1()
		self.local_debugger.send_to_monitor('step1')
		is_negotiation = self.selection_step2()
		self.local_debugger.send_to_monitor('step2')
		is_agreement = self.selection_step3()
		self.local_debugger.send_to_monitor('step3')
		if is_agreement == False:
			while is_negotiation:
				self.local_negotiation = self.local_negotiation + 1
				self.selection_step1()
				is_negotiation = self.selection_step2()
				is_agreement = self.selection_step3()
				if is_agreement == True:
					break
				else:
					continue
		self.local_debugger.send_to_monitor('step_execution')
		self.selection_execution()
		self.local_debugger.send_to_monitor('task_id, my_group_num: (%d, %d)' % (self.local_task_id, self.global_group_num_robots))

	def selection_execution(self):
		n = self.global_num_robots
		p = [self.global_energy_level[self.local_queue[0]]] * n
		k = self.global_num_tasks
		M = [[0 for i in range(k)] for j in range(n)]
		D = [[0 for i in range(k)] for j in range(n)]

		energy_sum = []
		partition_plan = []

		energy_level_queue = [self.global_energy_level[self.local_queue[i]] for i in range(n)]

		for i in range(1, n):
			p[i] = p[i-1] + energy_level_queue[i]
		
		for i in range(n):
			M[i][0] = p[i]

		for i in range(k):
			M[0][i] = energy_level_queue[i]

		for i in range(1, n):
			for j in range(1, k):
				M[i][j] = float('inf')
				for x in range(i):
					s = max(M[x][j-1], p[i]-p[x])
					if M[i][j] > s:
						M[i][j] = s
						D[i][j] = x

		partition_plan = []
		while k > 1:
			partition_plan.append(D[n-1][k-1])
			n = D[n-1][k-1] + 1
			k = k - 1
		partition_plan.reverse()

		myindex_in_queue = 0
		for i in range(self.global_num_robots):
			if self.local_id == self.local_queue[i]:
				myindex_in_queue = i
				break

		self.local_task_id = 0
		for i in range(self.global_num_tasks - 1):
			if myindex_in_queue > partition_plan[i]:
				self.local_task_id = self.local_task_id + 1
		

		if self.local_task_id == 0:
			my_group_num = partition_plan[0] + 1
		elif self.local_task_id == self.global_num_tasks - 1:
			my_group_num = self.global_num_robots - partition_plan[-1] - 1
		else:
			my_group_num = partition_plan[self.local_task_id] - partition_plan[self.local_task_id - 1]
		self.global_group_num_robots = my_group_num
			
	def check_recv_all_energy(self, recv_data):
		try:
			recv_id = recv_data['id']
			self.global_energy_level[recv_id] = recv_data['energy']
			if len(self.global_energy_level) == self.global_num_robots:
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_all_queue(self, recv_data):
		try:
			recv_id = recv_data['id']
			self.global_negotiation_queue[recv_id] = recv_data['queue']
			if len(self.global_negotiation_queue) == self.global_num_robots:
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_all_agreement(self, recv_data):
		try:
			recv_id = recv_data['id']
			self.global_agreement[recv_id] = recv_data['end']
			if len(self.global_agreement) == self.global_num_robots:
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	# Step1: Exchange energy level
	def selection_step1(self):
		send_data = self.get_basic_status()
		send_data['energy'] = self.local_energy_level
		self.message_communication(send_data, condition_func=self.check_recv_all_energy, time_out=3)
		if self.local_negotiation == 1:
			self.local_queue = [i[0] for i in sorted(self.global_energy_level.items(), key=lambda x:x[1])]
		elif self.local_negotiation == 2:
			self.local_queue = sorted(self.global_energy_level.iteritems(), key=lambda x:(x[1], x[0]), reverse = True)
		# TODO: 
		# 	clear energy_level at the appropriate moment
		# self.global_energy_level = {}

	# Step2: Exchange priority queue
	def selection_step2(self):
		send_data = self.get_basic_status()
		send_data['queue'] = self.local_queue
		self.message_communication(send_data, condition_func=self.check_recv_all_queue, time_out=3)
		for key in self.global_negotiation_queue.keys():
			if self.local_queue == self.global_negotiation_queue[key]:
				self.local_negotiation_result = True
			else:
				self.local_negotiation_result = False
		self.global_negotiation_queue = {}
		return self.local_negotiation_result

	# Step3: Agreement
	def selection_step3(self):
		send_data = self.get_basic_status()
		send_data['end'] = self.local_negotiation_result
		self.message_communication(send_data, condition_func=self.check_recv_all_agreement, time_out=3)
		is_agreement = True
		for value in self.global_agreement.values():
			if value == False:
				is_agreement = False
				break
		self.global_negotiation_queue = {}
		return is_agreement

	def formation(self):
		pass

	def formation_step1(self):
		pass

	def formation_step2(self):
		pass

	def formation_step3(self):
		pass

	def routing(self):
		pass

	def routing_step1(self):
		pass

	def routing_step2(self):
		pass

	def routing_step3(self):
		pass

	def walk_one_step(self):
		L2norm = math.sqrt(self.local_direction[0] * self.local_direction[0] + self.local_direction[1] * self.local_direction[1])
		if L2norm != 0:
			self.local_coordinate[0] = self.local_coordinate[0] + self.local_step_size * self.local_direction[0] / L2norm
			self.local_coordinate[1] = self.local_coordinate[1] + self.local_step_size * self.local_direction[1] / L2norm
			core_cmd = "coresendmsg -a %s node number=%s xpos=%s ypos=%s" % (self.controlNet, \
																		self.local_id, \
																		str(int(self.local_coordinate[0])), \
																		str(int(self.local_coordinate[1])))
			# self.local_debugger.send_to_monitor(core_cmd)
			os.system(core_cmd)
		else:
			# If direction vector is 0-vector, keep in place
			pass
		

if __name__ == '__main__':
	index = socket.gethostname()[1:]
	coordinate = [[50,50*i] for i in range(1,21,1)]
	strategy_SRSS = Strategy_SRSS(id=int(index), \
								coordinate=coordinate[int(index)-1], \
								direction=[1, 3], \
								step_size=10, \
								go_interval=0.5, \
								num_robots=20, \
								controlNet='172.16.0.254')
	while not strategy_SRSS.checkFinished():
		strategy_SRSS.go()




