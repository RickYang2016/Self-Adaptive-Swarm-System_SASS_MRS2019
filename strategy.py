#!/usr/bin/env python3

#Author: Zhiwei Luo

from task import Strategy, NetworkInterface
from COREDebugger import COREDebuggerVirtual
import time
import os
import math
import sys
import random
import socket
import numpy as np
from shapely.geometry import Polygon
from union import unionfind

class Strategy_SRSS(Strategy):
	network = None
	controlNet = None
	send_data_history = None
	time_start = None 					# For task release simulation -> Future work: real dynamic change.

	local_id = 0
	local_task_id = 0
	local_energy_level = 100
	local_direction = [1, 0]			# Direction vector: not necessary to be normalized
	local_robot_radius = 10				# not in __init__
	local_coordinate = [0, 0]
	local_task_destination = [0, 0]
	local_step_size = 1
	local_go_interval = 0.5
	local_round = 0
	local_stage = 'start'
	local_step = 0
	local_negotiation = 1
	local_has_gone = 0					# How many steps you go
	local_queue = []					# [3, 1, 2] means the priority: robot-3 > robot-1 > robot-2	
	local_negotiation_result = False	# If all the queues are the same, set as True, otherwise, False
	local_collision_queue = []			# Only contains local collision queue

	global_num_robots = 1 
	global_num_tasks = 0
	global_min_require_robots = 1
	global_group_num_robots = 1
	global_energy_level = {}			# {1: 100, 2: 99, 3: 85, ...}
	global_negotiation_queue = {}		# {'1': [3, 1, 2], '2': [3, 2, 1], '3': [3, 1, 2], ...}
	global_agreement = {}				# {'1': True, '2': False, '3': True, ...}
	global_task_list = []				# [{'duration': 100, 'raduis': 20, 'coordinate': [100, 100]}, {'duration': 150, 'raduis': 30, 'coordinate': [200, 150]}, ...]
	global_new_task_list = []			# Same as 
	global_robots_task_distance = {}	# Used in formation: the distance matrix - robots vs. location of the task
	global_robots_coordinate = {}		# {1: [xx, yy], ...}
	global_robots_polygon = {}			# {1: [(x1, y1), (x2, y2), (x3, y3), (x4, y4)], ...}
	global_collision_queue = {}			# {1: [3, 1], 2: [], 3: [3, 4], ...}
	global_robots_task_id = {}			# {1: 2, 2:1, 3:1, ...} Only used in routing - first priority
	global_deadlock = {}
	global_is_finish_task = {}			# {1: True, 4: False, 8: False} Only consider about my group
	global_time_step = 0				# For better logging and collecting data

	local_debugger = None

	def __init__(self, id, \
				coordinate=[50, 50], \
				direction=[1, 1], \
				step_size=1, \
				robot_radius=10, \
				energy_level=100, \
				go_interval=0.5, \
				num_robots=1, \
				controlNet='172.16.0.254'):
		self.local_id = id
		self.local_coordinate = coordinate
		self.local_direction = direction
		self.local_step_size = step_size
		self.local_robot_radius = robot_radius
		self.local_energy_level = energy_level
		self.local_go_interval = go_interval
		self.global_num_robots = num_robots
		self.controlNet = controlNet
		self.network = NetworkInterface(port=19999)
		self.network.initSocket()
		self.network.startReceiveThread()
		# Debugger tool:
		self.local_debugger = COREDebuggerVirtual((controlNet, 12888), path='/home/zhiwei/SRSS/log', filename=str(self.local_id))
		self.time_start = time.time()
		self.local_debugger.log_local('Start.', tag='Status')
		self.local_debugger.send_to_monitor({'id': self.local_id, 'coordinate': self.local_coordinate}, tag='Status')

	def checkFinished(self):
		return (math.fabs(self.local_task_destination[0] - self.local_coordinate[0]) < self.local_step_size and \
				math.fabs(self.local_task_destination[1] - self.local_coordinate[1]) < self.local_step_size)

	def go(self):
		self.local_debugger.log_local('%.2f' % self.local_energy_level, tag='Battery Energy')
		if self.local_stage == 'start':
			# Wait until new task arrives
			if self.global_num_tasks > 0:
				self.local_stage = 'selection'
			else:
				self.local_energy_level = self.local_energy_level - 0.04
				time.sleep(1)
			# self.global_condition_func()
		elif self.local_stage == 'selection':
			self.global_is_finish_task = {}
			self.local_round = self.local_round + 1
			self.local_debugger.log_local('Selection Start.', tag='Status')
			self.selection()
			self.local_debugger.log_local('Selection End: Do Task %d.' % self.local_task_id, tag='Status')
			self.local_stage = 'formation'
		elif self.local_stage == 'formation':
			self.local_debugger.log_local('Formation Start.', tag='Status')
			self.formation()
			# Formation End printed in formation step3
			self.local_stage = 'routing'
		elif self.local_stage == 'routing':
			self.global_time_step = self.global_time_step + 1
			self.local_debugger.log_local('Routing Start.', tag='Status')
			if self.checkFinished():
				self.local_debugger.send_to_monitor('I finished my task!')
				self.local_debugger.log_local('Task Finished.', tag='Status')
				self.local_stage = 'end'
			else:
				if not self.check_new_tasks():
					self.broadcast_coordinate()	# should broadcast original coodinate and polygon before routing.
				else:
					self.reallocate_tasks()
					return
				if not self.check_new_tasks():
					self.broadcast_polygon()
				else:
					self.reallocate_tasks()
					return
				if not self.check_new_tasks():
					self.routing()
				else:
					self.reallocate_tasks()
					return
		elif self.local_stage == 'end':
			self.global_time_step = self.global_time_step + 1
			if not self.check_new_tasks():
				self.broadcast_coordinate()
			else:
				self.reallocate_tasks()
				return
			if not self.check_new_tasks():
				self.broadcast_polygon()
			else:
				self.reallocate_tasks()
				return
			if not self.check_new_tasks():
				self.routing()
			else:
				self.reallocate_tasks()
				return
			# default stage is 'end'
			# if new tasks are released: local_stage -> 'start'
		else:
			print('Unknown state.')
		time.sleep(self.local_go_interval)
		self.reallocate_tasks()
		
	def reallocate_tasks(self):
		if self.local_stage != 'selection' and self.local_stage != 'formation':
			num_tasks_now = sum([i['start'] <= time.time()-self.time_start for i in self.global_task_list])
			if self.global_num_tasks != num_tasks_now:
				self.global_num_tasks = num_tasks_now
				self.local_stage = 'selection'
				self.local_debugger.log_local('A New Task Released.', tag='Task')
				self.local_debugger.send_to_monitor('A New Task Released.', tag='Task')
		if self.local_id == 1:
			if self.global_num_tasks != 0:
				self.local_debugger.send_to_monitor({'new_task': True, 'coordinate': [int(self.global_task_list[self.global_num_tasks-1]['coordinate'][0]), \
																				 	 int(self.global_task_list[self.global_num_tasks-1]['coordinate'][1])]}, tag='Status')

	def check_new_tasks(self):
		if self.local_stage != 'selection' and self.local_stage != 'formation':
			num_tasks_now = sum([i['start'] <= time.time()-self.time_start for i in self.global_task_list])
			if self.global_num_tasks != num_tasks_now:
				return True
			else:
				return False
		else:
			return False

	def check_recv_is_finish_task(self):
		if sum([i == True for i in self.global_is_finish_task.values()]) == self.global_group_num_robots:
			return True
		else:
			return False

	def global_condition_func(self, recv_data):
		pass

	def message_communication(self, send_data, condition_func, time_out=10):
		# input: send_data is a dictionary
		# output: recv_data is also a dictionary
		# new task release: trigger a new round of <selection-formation-routing>
		while True:
			self.local_energy_level = self.local_energy_level - 0.01
			# This is for preventing them to stuck here if everyone finished task
			if self.check_new_tasks():
				return
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
		is_negotiation = self.selection_step2()
		is_agreement = self.selection_step3()
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
		self.local_negotiation = 1
		self.selection_execution()
		# After this step, we get (self.local_task_id, self.global_group_num_robots)
		self.local_debugger.send_to_monitor('selection: ' + str((self.local_task_id, self.global_group_num_robots)))
		self.global_energy_level = {}
		self.global_agreement = {}
		# clear energy level data for future use.

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

		# If only one task
		if len(partition_plan) == 0:
			self.global_group_num_robots = self.global_num_robots
		else:
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
		self.message_communication(send_data, condition_func=self.check_recv_all_energy, time_out=0.01)
		if self.local_negotiation == 1:
			self.local_queue = [i[0] for i in sorted(self.global_energy_level.items(), key=lambda x:x[1])]
		elif self.local_negotiation == 2:
			self.local_queue = [i[0] for i in sorted(self.global_energy_level.items(), key=lambda x:(x[1], x[0]))]

	# Step2: Exchange priority queue
	def selection_step2(self):
		send_data = self.get_basic_status()
		send_data['queue'] = self.local_queue
		self.message_communication(send_data, condition_func=self.check_recv_all_queue, time_out=0.01)
		self.local_negotiation_result = False
		for key in self.global_negotiation_queue.keys():
			if self.local_queue == self.global_negotiation_queue[key]:
				continue
			else:
				self.local_negotiation_result = True
				break
		self.global_negotiation_queue = {}
		return self.local_negotiation_result

	# Step3: Agreement
	def selection_step3(self):
		send_data = self.get_basic_status()
		send_data['end'] = self.local_negotiation_result
		self.message_communication(send_data, condition_func=self.check_recv_all_agreement, time_out=0.01)
		is_agreement = True
		for value in self.global_agreement.values():
			if value == True:
				is_agreement = False
				break
		self.global_agreement = {}
		return is_agreement

	def check_recv_mygroup_energy(self, recv_data):
		try:
			recv_id = recv_data['id']
			recv_task_id = recv_data['task_id']
			# throw out the packet that has different task_id
			if recv_task_id != self.local_task_id:
				return
			self.global_energy_level[recv_id] = recv_data['energy']
			if len(self.global_energy_level) == self.global_group_num_robots:
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_mygroup_queue(self, recv_data):
		try:
			recv_id = recv_data['id']
			recv_task_id = recv_data['task_id']
			# throw out the packet that has different task_id
			if recv_task_id != self.local_task_id:
				return
			self.global_negotiation_queue[recv_id] = recv_data['queue']
			if len(self.global_negotiation_queue) == self.global_group_num_robots:
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_mygroup_agreement(self, recv_data):
		try:
			recv_id = recv_data['id']
			recv_task_id = recv_data['task_id']
			# throw out the packet that has different task_id
			if recv_task_id != self.local_task_id:
				return
			self.global_agreement[recv_id] = recv_data['end']
			if len(self.global_agreement) == self.global_group_num_robots:
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_mygroup_distance(self, recv_data):
		try:
			recv_id = recv_data['id']
			recv_task_id = recv_data['task_id']
			# throw out the packet that has different task_id
			if recv_task_id != self.local_task_id:
				return
			self.global_robots_task_distance[recv_id] = recv_data['dist']
			if len(self.global_robots_task_distance) == self.global_group_num_robots:
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def formation(self):
		self.formation_step1()
		is_negotiation = self.formation_step2()
		is_agreement = self.formation_step3()
		if is_agreement == False:
			while is_negotiation:
				self.local_negotiation = self.local_negotiation + 1
				self.formation_step1()
				is_negotiation = self.formation_step2()
				is_agreement = self.formation_step3()
				if is_agreement == True:
					break
				else:
					continue
		self.local_negotiation = 1
		self.formation_execution()
		# After this step, we get (self.local_task_id, self.global_group_num_robots)
		self.global_energy_level = {}
		# clear energy level data for future use.
		self.global_agreement = {}
		self.global_robots_task_distance = {}

	def formation_execution(self):
		# Computing the distances to the different task locations
		dist_vector = []
		for i in range(self.global_group_num_robots):
			theta = (2 * math.pi) / self.global_group_num_robots * i
			task_coordinate = np.array(self.global_task_list[self.local_task_id]['coordinate'])
			task_radius = self.global_task_list[self.local_task_id]['radius']
			task_destination = task_coordinate + np.array([task_radius * math.cos(theta), task_radius * math.sin(theta)])
			task_dist = np.linalg.norm(task_destination - np.array(self.local_coordinate))
			dist_vector.append(task_dist)
		# Send the distance vector to others
		send_data = self.get_basic_status()
		send_data['dist'] = dist_vector
		send_data['task_id'] = self.local_task_id
		self.message_communication(send_data, condition_func=self.check_recv_mygroup_distance, time_out=0.01)
		dist_matrix = self.global_robots_task_distance
		# Everyone look at the distance matrix and use the consensus queue to sequentially choose task.
		myindex_in_queue = 0
		for i in self.local_queue:
			task_chosen = dist_matrix[i].index(min(dist_matrix[i]))
			if i == self.local_id:
				myindex_in_queue = task_chosen
				break
			for j in dist_matrix:
				dist_matrix[j][task_chosen] = float('inf')
		theta = (2 * math.pi) / self.global_group_num_robots * myindex_in_queue
		my_task_coordinate = self.global_task_list[self.local_task_id]['coordinate']
		my_task_radius = self.global_task_list[self.local_task_id]['radius']
		self.local_task_destination[0] = my_task_coordinate[0] + my_task_radius * math.cos(theta)
		self.local_task_destination[1] = my_task_coordinate[1] + my_task_radius * math.sin(theta)
		self.local_direction[0] = self.local_task_destination[0] - self.local_coordinate[0]
		self.local_direction[1] = self.local_task_destination[1] - self.local_coordinate[1]
		self.local_debugger.send_to_monitor('formation: index = ' + str(myindex_in_queue))
		self.local_debugger.log_local('Formation End: To Position %d.' % myindex_in_queue, tag='Status')

	def formation_step1(self):
		send_data = self.get_basic_status()
		send_data['energy'] = self.local_energy_level
		send_data['task_id'] = self.local_task_id
		self.message_communication(send_data, condition_func=self.check_recv_mygroup_energy, time_out=0.01)
		if self.local_negotiation == 1:
			self.local_queue = [i[0] for i in sorted(self.global_energy_level.items(), key=lambda x:x[1])]
		elif self.local_negotiation == 2:
			self.local_queue = [i[0] for i in sorted(self.global_energy_level.items(), key=lambda x:(x[1], x[0]))]

	def formation_step2(self):
		send_data = self.get_basic_status()
		send_data['queue'] = self.local_queue
		send_data['task_id'] = self.local_task_id
		self.message_communication(send_data, condition_func=self.check_recv_mygroup_queue, time_out=0.01)
		self.local_negotiation_result = False
		for key in self.global_negotiation_queue.keys():
			if self.local_queue == self.global_negotiation_queue[key]:
				continue
			else:
				self.local_negotiation_result = True
				break
		self.global_negotiation_queue = {}
		return self.local_negotiation_result

	def formation_step3(self):
		send_data = self.get_basic_status()
		send_data['end'] = self.local_negotiation_result
		send_data['task_id'] = self.local_task_id
		self.message_communication(send_data, condition_func=self.check_recv_mygroup_agreement, time_out=0.01)
		is_agreement = True
		for value in self.global_agreement.values():
			if value == True:
				is_agreement = False
				break
		self.global_agreement = {}
		return is_agreement

	def check_recv_robots_coordinates(self, recv_data):
		try:
			recv_id = recv_data['id']
			recv_coordinate = recv_data['coordinate']
			recv_task_id = recv_data['task_id']
			recv_is_finished = recv_data['is_finish']
			# throw out the packet that has different task_id
			self.global_robots_coordinate[recv_id] = recv_coordinate
			if recv_task_id == self.local_task_id:
				self.global_is_finish_task[recv_id] = recv_data['is_finish']
			if len(self.global_robots_coordinate) == self.global_num_robots:
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_robots_polygons(self, recv_data):
		try:
			recv_id = recv_data['id']
			recv_polygon = recv_data['polygon']
			# throw out the packet that has different task_id
			self.global_robots_polygon[recv_id] = recv_polygon
			if len(self.global_robots_polygon) == self.global_num_robots:
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_collision_queue(self, recv_data):
		try:
			recv_id = recv_data['id']
			recv_collision = recv_data['collision_queue']
			# throw out the packet that has different task_id
			self.global_collision_queue[recv_id] = recv_collision
			if len(self.global_collision_queue) == self.global_num_robots:
				return True
			else: 
				#self.local_debugger.send_to_monitor('collision_queue: %d %d' % (len(self.global_collision_queue), self.global_num_robots))
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_local_collision_task_id(self, recv_data):
		try:
			recv_id = recv_data['id']
			recv_task_id = recv_data['task_id']
			# throw out the packet that has different task_id
			if recv_id in self.local_collision_queue:
				self.global_robots_task_id[recv_id] = recv_task_id
			if len(self.global_robots_task_id) == len(self.local_collision_queue):
				return True
			else:
				#self.local_debugger.send_to_monitor('collision_taskid: %d %d' % (len(self.global_robots_task_id), len(self.local_collision_queue)))
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_local_collision_energy(self, recv_data):
		try:
			recv_id = recv_data['id']
			# throw out the packet that has different task_id
			if recv_id in self.local_collision_queue:
				self.global_energy_level[recv_id] = recv_data['energy']
			if len(self.global_energy_level) == len(self.local_collision_queue):
				return True
			else:
				#self.local_debugger.send_to_monitor('collision_taskid: %d %d' % (len(self.global_robots_task_id), len(self.local_collision_queue)))
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_local_collision_queue(self, recv_data):
		try:
			recv_id = recv_data['id']
			if recv_id in self.local_collision_queue:
				self.global_negotiation_queue[recv_id] = recv_data['queue']
			if len(self.global_negotiation_queue) == len(self.local_collision_queue):
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_local_collision_agreement(self, recv_data):
		try:
			recv_id = recv_data['id']
			if recv_id in self.local_collision_queue:
				self.global_agreement[recv_id] = recv_data['end']
			if len(self.global_agreement) == len(self.local_collision_queue):
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def check_recv_deadlock(self, recv_data):
		try:
			recv_id = recv_data['id']
			if recv_id in self.local_collision_queue:
				self.global_deadlock[recv_id] = recv_data['deadlock']
			if len(self.global_deadlock) == len(self.local_collision_queue):
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def routing(self):
		self.routing_step1()
		is_collision = self.routing_step2()		# Generate a local collision queue with in-group consensus
		if is_collision == True:
			self.routing_step3()				# Generate a priority queue
			is_negotiation = self.routing_step4()
			is_agreement = self.routing_step5()
			if is_agreement == False:
				while is_negotiation:
					self.local_negotiation = self.local_negotiation + 1
					self.routing_step3()
					is_negotiation = self.routing_step4()
					is_agreement = self.routing_step5()
					if is_agreement == True:
						break
					else:
						continue
			self.local_negotiation = 1
			self.routing_execution()
			self.global_collision_queue = {}
			self.global_robots_task_id = {}
			self.global_energy_level = {}
			self.global_negotiation_queue = {}
			self.global_agreement = {}
			self.global_deadlock = {}
		else:
			self.walk_one_step()

	def rectangle_transform(self, rectangle, direction, local_coordinate):
		vertices = np.transpose(np.array([[rectangle[0][0], rectangle[0][1]], \
										  [rectangle[1][0], rectangle[1][1]], \
										  [rectangle[2][0], rectangle[2][1]], \
										  [rectangle[3][0], rectangle[3][1]]]))
		rotation_matrix = np.array([[math.cos(direction), - math.sin(direction)], \
									[math.sin(direction), math.cos(direction)]])
		new_vertices = np.matmul(rotation_matrix, vertices)
		update_coordinate = np.transpose(new_vertices + [[local_coordinate[0]], [local_coordinate[1]]])

		return update_coordinate

	def vector_transform(self, vector, direction, local_coordinate):
		vertices = np.transpose(np.array([[vector[0][0], vector[0][1]], \
										  [vector[1][0], vector[1][1]]]))
		rotation_matrix = np.array([[math.cos(direction), - math.sin(direction)], \
									[math.sin(direction), math.cos(direction)]])
		new_vertices = np.matmul(rotation_matrix, vertices)
		update_coordinate = np.transpose(new_vertices + [[local_coordinate[0]], [local_coordinate[1]]])

		return update_coordinate

	# Step1: Collision Detection
	def routing_step1(self):
		if self.local_direction[0] != 0:
			direction_angle = math.atan(self.local_direction[1] / self.local_direction[0])
		else:
			direction_angle = 0
		my_raw_rectangle = [[-self.local_robot_radius, self.local_robot_radius], 
							[-self.local_robot_radius, -self.local_robot_radius],
							[self.local_robot_radius + self.local_step_size, -self.local_robot_radius],
							[self.local_robot_radius + self.local_step_size, self.local_robot_radius]]
		my_rectangle = self.rectangle_transform(my_raw_rectangle, direction_angle, self.local_coordinate)
		p1 = Polygon([	(my_rectangle[0][0], my_rectangle[0][1]), 
						(my_rectangle[1][0], my_rectangle[1][1]), 
						(my_rectangle[2][0], my_rectangle[2][1]), 
						(my_rectangle[3][0], my_rectangle[3][1])])
			
		self.local_queue = []
		for index in range(self.global_num_robots):
			i = index + 1
			if i != self.local_id:
				p2 = Polygon(self.global_robots_polygon[i])
				if p1.intersects(p2):
					self.local_queue.append(i)
		if len(self.local_queue) > 0:
			self.local_queue.append(self.local_id)
		# After this step, only get the "potential" collision queue

	# Generate local collision queue: unique 'set' but is not unique 'queue'
	def routing_step2(self):
		send_data = self.get_basic_status()
		send_data['collision_queue'] = self.local_queue
		self.global_collision_queue = {}
		self.message_communication(send_data, condition_func=self.check_recv_collision_queue, time_out=0.01)
		u = unionfind(self.global_collision_queue.values())
		u.createtree()
		collision_queues = u.printree()
		self.local_collision_queue = []
		for queue in collision_queues:
			if self.local_id in queue:
				self.local_collision_queue = queue
				break
		# After this step, get the final local consensus collision queue
		if len(self.local_collision_queue) > 0:
			return True
		else:
			return False

	# Communicate task id as the first priority
	def routing_step3(self):
		send_data = self.get_basic_status()
		send_data['task_id'] = self.local_task_id
		self.global_robots_task_id = {}
		# TODO: check_recv_local_collision_task_id not exists
		self.message_communication(send_data, condition_func=self.check_recv_local_collision_task_id, time_out=0.01)
		send_data = self.get_basic_status()
		send_data['energy'] = self.local_energy_level
		self.global_energy_level = {}
		# TODO: check_recv_local_collision_task_id not exists
		self.message_communication(send_data, condition_func=self.check_recv_local_collision_energy, time_out=0.01)
		taskid_energy = [(i, self.global_robots_task_id[i], self.global_energy_level[i]) for i in self.local_collision_queue]
		if self.local_negotiation == 1:
			self.local_queue = [i[0] for i in sorted(taskid_energy, key=lambda x:(x[1], x[2], x[0]))]
		elif self.local_negotiation == 2:
			self.local_queue = [i[0] for i in sorted(taskid_energy, key=lambda x:(x[2], x[0]))]

	# Exchange Priority queue: Exactly same as selection part - step2
	def routing_step4(self):
		send_data = self.get_basic_status()
		send_data['queue'] = self.local_queue
		self.message_communication(send_data, condition_func=self.check_recv_local_collision_queue, time_out=0.01)
		self.local_negotiation_result = False
		for key in self.global_negotiation_queue.keys():
			if self.local_queue == self.global_negotiation_queue[key]:
				continue
			else:
				self.local_negotiation_result = True
				break
		self.global_negotiation_queue = {}
		return self.local_negotiation_result

	# Agreement: Also the same as selection - step3
	def routing_step5(self):
		send_data = self.get_basic_status()
		send_data['end'] = self.local_negotiation_result
		self.message_communication(send_data, condition_func=self.check_recv_local_collision_agreement, time_out=0.01)
		is_agreement = True
		for value in self.global_agreement.values():
			if value == True:
				is_agreement = False
				break
		self.global_agreement = {}
		return is_agreement

	def routing_execution(self):
		# Loop until deadlock dismisses
		while True:
			self.global_deadlock = {}
			if self.local_id == self.local_queue[0]:
				dist_queue = {}
				for robot_id in self.local_queue:
					if robot_id != self.local_id:
						dist = np.linalg.norm([self.global_robots_coordinate[robot_id][0][1] - self.local_coordinate[1], \
												self.global_robots_coordinate[robot_id][0][0] - self.local_coordinate[0]])
						dist_queue[robot_id] = dist
				ordered_queue = [i[0] for i in sorted(dist_queue.items(), key=lambda x:x[1])]

				is_deadlock = True
				if not self.checkFinished():
					closest_robot_coordinate = np.array(self.global_robots_coordinate[ordered_queue[0]][0])
					my_coordinate = np.array(self.local_coordinate)
					my_direction = np.array(self.local_direction)

					# theta = boundary tangent angle not to collide
					theta = math.atan(2 * self.local_robot_radius / (np.linalg.norm(closest_robot_coordinate - my_coordinate) - self.local_robot_radius * 2))

					# theta1 = acos(a`b/(|a||b|))
					relative_direction = closest_robot_coordinate - my_coordinate
					theta1 = math.acos(np.inner(my_direction, relative_direction) / (np.linalg.norm(my_direction) * np.linalg.norm(relative_direction)))
					if self.local_direction[0] != 0:
						my_angle = math.atan(self.local_direction[1] / self.local_direction[0])
					else:
						my_angle = math.pi / 2

					if theta1 < theta:
						new_angle = my_angle + theta - theta1 + 10 * math.pi / 180
					else:
						new_angle = my_angle

					self.local_direction = [math.cos(new_angle), math.sin(new_angle)]
					is_deadlock = False
				else: # I have finish. I will not move
					is_deadlock = True

				send_data = self.get_basic_status()
				send_data['deadlock'] = is_deadlock
				self.message_communication(send_data, condition_func=self.check_recv_deadlock, time_out=0.01)

				if is_deadlock == False:
					self.walk_one_step()
					break
				else:
					# shift my local_queue: put myself to the last
					self.local_queue = self.local_queue[1:] + self.local_queue[0:1]
			else:
				# I am not the first one in queue
				send_data = self.get_basic_status()
				send_data['deadlock'] = False
				self.message_communication(send_data, condition_func=self.check_recv_deadlock, time_out=0.01)
				# The first one in queue has deadlock -> shift
				if self.global_deadlock[self.local_queue[0]] == True:
					self.local_queue = self.local_queue[1:] + self.local_queue[0:1]
				else:
					# deadlock released, keep in place
					self.local_debugger.log_local('Routing %d: Walk: %d' % (self.global_time_step, self.local_has_gone), tag='Status')
					self.local_energy_level = self.local_energy_level - 0.04
					break

	def broadcast_coordinate(self):
		# Coordinates of current and next
		L2norm = math.sqrt(self.local_direction[0] * self.local_direction[0] + self.local_direction[1] * self.local_direction[1])
		if L2norm != 0 and not self.checkFinished():
			cur_next_coordinate = [[self.local_coordinate[0], self.local_coordinate[1]], \
									[self.local_coordinate[0] + self.local_step_size * self.local_direction[0] / L2norm, \
									 self.local_coordinate[1] + self.local_step_size * self.local_direction[1] / L2norm]]
		else:
			cur_next_coordinate = [[self.local_coordinate[0], self.local_coordinate[1]], \
								[self.local_coordinate[0], self.local_coordinate[1]]]
		send_data = self.get_basic_status()
		send_data['coordinate'] = cur_next_coordinate
		send_data['task_id'] = self.local_task_id
		send_data['is_finish'] = self.checkFinished()
		self.global_robots_coordinate = {}
		self.message_communication(send_data, condition_func=self.check_recv_robots_coordinates, time_out=0.01)

	def broadcast_polygon(self):
		# Polygon 
		send_data = self.get_basic_status()
		if self.local_direction[0] != 0:
			direction_angle = math.atan(self.local_direction[1] / self.local_direction[0])
		else:
			direction_angle = 0
		my_raw_rectangle = [[-self.local_robot_radius, self.local_robot_radius], 
							[-self.local_robot_radius, -self.local_robot_radius],
							[self.local_robot_radius + self.local_step_size, -self.local_robot_radius],
							[self.local_robot_radius + self.local_step_size, self.local_robot_radius]]
		my_rectangle = self.rectangle_transform(my_raw_rectangle, direction_angle, self.local_coordinate)
		polygon = [	(my_rectangle[0][0], my_rectangle[0][1]), 
					(my_rectangle[1][0], my_rectangle[1][1]), 
					(my_rectangle[2][0], my_rectangle[2][1]), 
					(my_rectangle[3][0], my_rectangle[3][1])]
		send_data['polygon'] = polygon
		self.global_robots_polygon = {}
		self.message_communication(send_data, condition_func=self.check_recv_robots_polygons, time_out=0.01)

	def walk_one_step(self):
		if not self.checkFinished():
			L2norm = math.sqrt(self.local_direction[0] * self.local_direction[0] + self.local_direction[1] * self.local_direction[1])
			if L2norm != 0:
				self.local_coordinate[0] = self.local_coordinate[0] + self.local_step_size * self.local_direction[0] / L2norm
				self.local_coordinate[1] = self.local_coordinate[1] + self.local_step_size * self.local_direction[1] / L2norm
				# Return to the task direction even if you change direction in routing in last step
				self.local_direction[0] = self.local_task_destination[0] - self.local_coordinate[0]
				self.local_direction[1] = self.local_task_destination[1] - self.local_coordinate[1]
				self.local_debugger.send_to_monitor({'id': self.local_id, 'coordinate': self.local_coordinate}, tag='Status')
				self.local_debugger.log_local({'id': self.local_id, 'coordinate': self.local_coordinate}, tag='Status')
				self.local_energy_level = self.local_energy_level - 0.1
				self.local_has_gone = self.local_has_gone + 1
			else:
				# If direction vector is 0-vector, keep in place
				self.local_energy_level = self.local_energy_level - 0.04
				pass
		self.local_debugger.log_local('Routing %d: Walk: %d' % (self.global_time_step, self.local_has_gone), tag='Status')

if __name__ == '__main__':
	simulate_num_robots = 20
	index = socket.gethostname()[1:]
	# Use the current coordinate to compute
	with open('../n%d.xy' % int(index), 'r') as f:
		xy = f.read()
		coordinate = [int(float(xy.split(' ')[0])), int(float(xy.split(' ')[1]))]

	energy_level_equal = [100] * simulate_num_robots
	energy_level_random = [	[90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90], \
							[89, 90, 89, 90, 90, 87, 89, 88, 90, 90, 89, 90, 89, 91, 89, 89, 88, 90, 91, 90], \
							[89, 91, 86, 86, 90, 88, 88, 89, 93, 88, 89, 91, 89, 90, 86, 88, 91, 87, 90, 91], \
							[92, 89, 93, 84, 92, 89, 83, 88, 88, 91, 89, 91, 91, 91, 88, 87, 90, 88, 88, 87], \
							[92, 91, 95, 88, 91, 91, 91, 94, 80, 93, 83, 90, 94, 88, 87, 92, 97, 89, 85, 93], \
							[96, 89, 84, 93, 80, 100, 84, 94, 89, 87, 81, 85, 100, 94, 93, 98, 89, 94, 86, 96], \
							[78, 85, 79, 98, 85, 90, 97, 86, 93, 94, 86, 85, 92, 90, 85, 85, 84, 86, 92, 93], \
							[81, 81, 94, 80, 95, 89, 87, 90, 92, 80, 80, 97, 72, 96, 79, 77, 92, 94, 98, 98], \
							[80, 86, 100, 82, 91, 85, 85, 90, 100, 84, 98, 83, 93, 78, 91, 96, 91, 82, 80, 84], \
							[85, 100, 80, 89, 86, 94, 84, 89, 90, 83, 77, 96, 93, 83, 76, 100, 97, 87, 97, 84], \
							[82, 79, 75, 93, 92, 88, 89, 72, 100, 84, 62, 88, 100, 100, 89, 65, 85, 96, 69, 100], \
							[92, 82, 83, 89, 93, 93, 80, 92, 92, 90, 94, 96, 99, 100, 97, 88, 95, 81, 100, 87]]

	energy_level = energy_level_random[:simulate_num_robots]
	strategy_SRSS = Strategy_SRSS(id=int(index), \
								coordinate=coordinate, \
								direction=[1, 3], \
								step_size=10, \
								robot_radius=10, \
								go_interval=0.1, \
								num_robots=simulate_num_robots, \
								energy_level=energy_level[11][int(index) - 1], \
								controlNet='172.16.0.254')
	strategy_SRSS.global_task_list = [{'start': 5, 'duration': 40, 'radius' : 200, 'coordinate': [325, 475], 'new_task': True},
									{'start': 30, 'duration': 10, 'radius' : 100, 'coordinate': [1200, 700], 'new_task': True},
									{'start': 60, 'duration': 10, 'radius' : 70, 'coordinate': [1075, 175], 'new_task': True}]
	# strategy_SRSS.global_task_list = [{'start': 5, 'duration': 40, 'radius' : 200, 'coordinate': [325, 475], 'new_task': True},
	# 								{'start': 5, 'duration': 10, 'radius' : 100, 'coordinate': [1200, 700], 'new_task': True},
	# 								{'start': 5, 'duration': 10, 'radius' : 70, 'coordinate': [1075, 175], 'new_task': True}]
	# strategy_SRSS.global_task_list = [{'start': 5, 'duration': 40, 'radius' : 200, 'coordinate': [325, 475], 'new_task': True}]
	# strategy_SRSS.global_num_tasks = len(strategy_SRSS.global_task_list)
	while True:
		strategy_SRSS.go()




