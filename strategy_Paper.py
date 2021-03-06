#!/usr/bin/env python3

#Author: Zhiwei Luo

from task import Strategy, NetworkInterface
from COREDebugger import COREDebuggerVirtual
import time
import os
import math
import sys
import socket
import numpy as np

class Strategy_SRSS(Strategy):
	network = None
	controlNet = None
	send_data_history = None

	local_id = 0
	local_task_id = 0
	local_energy_level = 100
	local_direction = [1, 0]			# Direction vector: not necessary to be normalized
	local_coordinate = [0, 0]
	local_task_destination = [0, 0]
	local_step_size = 1
	local_go_interval = 0.5
	local_round = 0
	local_stage = 'start'
	local_step = 0
	local_negotiation = 1
	local_queue = []					# [3, 1, 2] means the priority: robot-3 > robot-1 > robot-2	
	local_negotiation_result = False	# If all the queues are the same, set as True, otherwise, False

	global_num_robots = 1
	global_num_tasks = 1
	global_min_require_robots = 1
	global_group_num_robots = 1
	global_energy_level = {}			# {1: 100, 2: 99, 3: 85, ...}
	global_negotiation_queue = {}		# {'1': [3, 1, 2], '2': [3, 2, 1], '3': [3, 1, 2], ...}
	global_agreement = {}				# {'1': True, '2': False, '3': True, ...}
	global_task_duration = 10
	global_task_radius = 200
	global_task_coordinate = [400, 400]
	global_robots_coordinate = {}

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
		return (math.fabs(self.local_task_destination[0] - self.local_coordinate[0]) < 5 and \
				math.fabs(self.local_task_destination[1] - self.local_coordinate[1]) < 5)

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
			if self.checkFinished():
				self.local_debugger.send_to_monitor('I finished my task!')
				self.local_stage = 'end'
			else:
				self.routing()
		elif self.local_stage == 'end':
			self.broadcast_coordinate()
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
		self.message_communication(send_data, condition_func=self.check_recv_all_energy, time_out=3)
		if self.local_negotiation == 1:
			self.local_queue = [i[0] for i in sorted(self.global_energy_level.items(), key=lambda x:x[1])]
		elif self.local_negotiation == 2:
			self.local_queue = sorted(self.global_energy_level.iteritems(), key=lambda x:(x[1], x[0]), reverse = True)

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
			self.local_debugger.send_to_monitor('recv (id, task_id): ' + str((recv_id, recv_task_id)))
			self.global_agreement[recv_id] = recv_data['end']
			if len(self.global_agreement) == self.global_group_num_robots:
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

	def formation_execution(self):
		myindex_in_queue = 0
		for i in range(self.global_num_robots):
			if self.local_id == self.local_queue[i]:
				myindex_in_queue = i
				break
		theta = (2 * math.pi) / self.global_group_num_robots * myindex_in_queue
		self.local_task_destination[0] = self.global_task_coordinate[0] + self.global_task_radius * math.cos(theta)
		self.local_task_destination[1] = self.global_task_coordinate[1] + self.global_task_radius * math.sin(theta)
		self.local_direction[0] = self.local_task_destination[0] - self.local_coordinate[0]
		self.local_direction[1] = self.local_task_destination[1] - self.local_coordinate[1]
		self.local_debugger.send_to_monitor('destination: ' + str(self.local_task_destination))

	def formation_step1(self):
		send_data = self.get_basic_status()
		send_data['energy'] = self.local_energy_level
		send_data['task_id'] = self.local_task_id
		self.message_communication(send_data, condition_func=self.check_recv_mygroup_energy, time_out=3)
		if self.local_negotiation == 1:
			self.local_queue = [i[0] for i in sorted(self.global_energy_level.items(), key=lambda x:x[1])]
		elif self.local_negotiation == 2:
			self.local_queue = sorted(self.global_energy_level.iteritems(), key=lambda x:(x[1], x[0]), reverse = True)

	def formation_step2(self):
		send_data = self.get_basic_status()
		send_data['queue'] = self.local_queue
		send_data['task_id'] = self.local_task_id
		self.message_communication(send_data, condition_func=self.check_recv_mygroup_queue, time_out=3)
		for key in self.global_negotiation_queue.keys():
			if self.local_queue == self.global_negotiation_queue[key]:
				self.local_negotiation_result = True
			else:
				self.local_negotiation_result = False
		self.global_negotiation_queue = {}
		return self.local_negotiation_result

	def formation_step3(self):
		send_data = self.get_basic_status()
		send_data['end'] = self.local_negotiation_result
		send_data['task_id'] = self.local_task_id
		self.message_communication(send_data, condition_func=self.check_recv_mygroup_agreement, time_out=3)
		is_agreement = True
		for value in self.global_agreement.values():
			if value == False:
				is_agreement = False
				break
		self.global_negotiation_queue = {}
		return is_agreement

	def check_recv_robots_coordinates(self, recv_data):
		try:
			recv_id = recv_data['id']
			recv_coordinate = recv_data['coordinate']
			# throw out the packet that has different task_id
			self.global_robots_coordinate[recv_id] = recv_coordinate
			if len(self.global_robots_coordinate) == self.global_group_num_robots:
				return True
			else:
				return False
		except KeyError:
			pass
		except Exception as e:
			raise e

	def routing(self):
		is_collision = self.routing_step1()
		if is_collision == True:
			is_negotiation = self.routing_step2()
			is_agreement = self.routing_step3()
			if is_agreement == False:
				while is_negotiation:
					self.local_negotiation = self.local_negotiation + 1
					self.routing_step1()
					is_negotiation = self.routing_step2()
					is_agreement = self.routing_step3()
					if is_agreement == True:
						break
					else:
						continue
			self.local_negotiation = 1
			self.routing_execution()
			# After this step, we get (self.local_task_id, self.global_group_num_robots)
			self.global_energy_level = {}
			# clear energy level data for future use.
			self.global_agreement = {}
		else:
			self.walk_one_step()

	def get_cross(p1, p2, p):
		return (p2[0] - p1[0]) * (p[1] - p1[1]) -(p[0] - p1[0]) * (p2[1] - p1[1])

	def inside_point(p1, p2, p3, p4, p):
		return  get_cross(p1, p2, p) * \
				get_cross(p3, p4, p) >= 0 \
				and
				get_cross(p2, p3, p) * \
				get_cross(p4, p1, p) >= 0 \

	def coordination_transform(p1, p2, p3, p4, direction, local_coordinate):
		vertices = np.transpose(np.array([[p1[0], p1[1]], \
										  [p2[0], p2[1]], \
										  [p3[0], p3[1]], \
										  [p4[0], p4[1]]]))
		rotation_matrix = np.array([[math.cos(direction), - math.sin(direction)], \
									[math.sin(direction), math.cos(direction)]])
		vertices = vertices - [[local_coordinate[0]], [local_coordinate[1]]]
		new_vertices = np.matmul(rotation_matrix, vertices)
		update_coordinate = np.transpose(new_vertices + [[local_coordinate[0]], [local_coordinate[1]]])

		return update_coordinate



	# Step1: Collision Detection
	def routing_step1(self):
		if self.local_direction[0] != 0:
			direction_angle = math.atan(self.local_direction[1] / self.local_direction[0])
		else:
			direction_angle = 0

		# Computing four vertices of the collision area: Rotation + Transformation
		# vertices = np.transpose(np.array([[-self.local_robot_radius, self.local_robot_radius], \
		# 								  [-self.local_robot_radius, -self.local_robot_radius], \
		# 								  [self.local_robot_radius + self.local_step_size, self.local_robot_radius], \
		# 								  [self.local_robot_radius + self.local_step_size, -self.local_robot_radius]]))
		# rotation_matrix = np.array([[math.cos(direction_angle), -math.sin(direction_angle)], \
		# 							[math.sin(direction_angle), math.cos(direction_angle)]])
		# new_vertices = np.matmul(rotation_matrix, vertices)
		# collision_vertices = np.transpose(new_vertices + [[self.local_coordinate[0]], [self.local_coordinate[1]]])

		vertices = np.transpose(np.array([[0, self.local_robot_radius], \
										  [0, -self.local_robot_radius], \
										  [self.local_robot_radius + self.local_step_size, self.local_robot_radius], \
										  [self.local_robot_radius + self.local_step_size, -self.local_robot_radius]]))
		rotation_matrix = np.array([[math.cos(direction_angle), -math.sin(direction_angle)], \
									[math.sin(direction_angle), math.cos(direction_angle)]])
		new_vertices = np.matmul(rotation_matrix, vertices)
		collision_vertices = np.transpose(new_vertices + [[self.local_coordinate[0]], [self.local_coordinate[1]]])

		# plu_x = self.local_coordinate[0] + math.sqrt(2) * self.local_robot_radius * math.cos(direction_angle + math.pi / 4)
		# plu_y = self.local_coordinate[1] + math.sqrt(2) * self.local_robot_radius * math.sin(direction_angle + math.pi / 4)
		# pld_x = self.local_coordinate[0] + math.sqrt(2) * self.local_robot_radius * math.cos(direction_angle - math.pi / 4)
		# pld_y = self.local_coordinate[1] + math.sqrt(2) * self.local_robot_radius * math.sin(direction_angle - math.pi / 4)
		# pru_x = plu_x + self.local_step_size * math.cos(direction_angle)
		# pru_y = plu_y + self.local_step_size * math.sin(direction_angle)
		# prd_x = pld_x + self.local_step_size * math.cos(direction_angle)
		# prd_y = pld_y + self.local_step_size * math.sin(direction_angle)

		# for index in range(self.global_num_robots):
		# 	i = index + 1
		# 	if (get_cross(collision_vertices[0], collision_vertices[1], self.global_robots_coordinate[i][0]) * \
		# 		get_cross(collision_vertices[2], collision_vertices[3], self.global_robots_coordinate[i][0]) >= 0 \
		# 		and
		# 		get_cross(collision_vertices[1], collision_vertices[2], self.global_robots_coordinate[i][0]) * \
		# 		get_cross(collision_vertices[3], collision_vertices[0], self.global_robots_coordinate[i][0]) >= 0) \
		# 		or 
		# 		(get_cross(collision_vertices[0], collision_vertices[1], self.global_robots_coordinate[i][1]) * \
		# 		get_cross(collision_vertices[2], collision_vertices[3], self.global_robots_coordinate[i][1]) >= 0 \
		# 		and
		# 		get_cross(collision_vertices[1], collision_vertices[2], self.global_robots_coordinate[i][1]) * \
		# 		get_cross(collision_vertices[3], collision_vertices[0], self.global_robots_coordinate[i][1]) >= 0) :
		# 		self.local_queue.append(i)

		for index in range(self.global_num_robots):
			i = index + 1
			if (inside_point(collision_vertices[0], collision_vertices[1], collision_vertices[2], collision_vertices[3], self.global_robots_coordinate[i][0])) \
				or 
				(inside_point(collision_vertices[0], collision_vertices[1], collision_vertices[2], collision_vertices[3], self.global_robots_coordinate[i][1])) :
				self.local_queue.append(i)

	def routing_step2(self):
		pass

	def routing_step3(self):
		pass

#input: sorted queue, current detecting range points, figure points and direction
#output: next step range points, figure points and direction
	def routing_execution(self):

		# for i in range(len(self.local_queue)):
		# 	theta = atan(2 * self.local_robot_radius / (math.sqrt(math.pow(self.local_coordinate[0] - self.local_queue[i][0], 2) 
		# 		+ math.pow(self.local_coordinate[1] - self.local_queue[i][1], 2)) - self.local_robot_radius * 2))

		# 	relative_direction = self.local_queue - self.local_direction

		# 	theta1 = acos(self.local_direction * relative_direction / math.sqrt(math.pow(self.local_coordinate[0], 2) + math.pow(self.local_coordinate[1], 2)) *
		# 		math.sqrt(math.pow(relative_direction[0], 2) + math.pow(relative_direction[1], 2)))
 			
 	# 		update_angle = atan(self.local_direction[1]/self.local_direction[0])

		# 	if theta1 <= theta && self.local_id == i:
		# 		update_angle = aten(self.local_direction[1]/self.local_direction[0]) + theta - theta1

		for i in range(len(self.local_queue)):
			theta = atan(2 * self.local_robot_radius / (np.linalg.norm(self.local_queue[i] - self.local_coordinate) - self.local_robot_radius * 2))

			relative_direction = self.local_queue[i] - self.local_coordinate

			theta1 = acos(self.local_direction * relative_direction / (np.linalg.norm(self.local_direction) * np.linalg.norm(relative_direction)))
 			
 			update_direction = atan(self.local_direction[1]/self.local_direction[0])

 			#next step rotate theta, move one step and update their next step coordination
			if theta1 <= theta && self.local_id == i:
				update_direction = atan(self.local_direction[1]/self.local_direction[0]) + theta - theta1

				vertices = np.transpose(np.array([[0, self.local_robot_radius], \
										  [0, -self.local_robot_radius], \
										  [self.local_robot_radius + 2 * self.local_step_size, self.local_robot_radius], \
										  [self.local_robot_radius + 2 * self.local_step_size, -self.local_robot_radius]]))
				rotation_matrix = np.array([[math.cos(update_direction), -math.sin(update_direction)], \
											[math.sin(update_direction), math.cos(update_direction)]])
				new_vertices = np.matmul(rotation_matrix, vertices)
				update_next_step_vertices = np.transpose(new_vertices + [[self.local_coordinate[0]], [self.local_coordinate[1]]])

 			#next step do not rotate theta, move one step and update their next step coordination
			elif theta1 >= theta && self.local_id == i:

				vertices = np.transpose(np.array([[0, self.local_robot_radius], \
										  [0, -self.local_robot_radius], \
										  [self.local_robot_radius + 2 * self.local_step_size, self.local_robot_radius], \
										  [self.local_robot_radius + 2 * self.local_step_size, -self.local_robot_radius]]))
				rotation_matrix = np.array([[math.cos(update_direction), -math.sin(update_direction)], \
											[math.sin(update_direction), math.cos(update_direction)]])
				new_vertices = np.matmul(rotation_matrix, vertices)
				update_next_step_vertices = np.transpose(new_vertices + [[self.local_coordinate[0]], [self.local_coordinate[1]]])

			#do not move in the next step
			else:

				update_next_step_vertices = self.local_coordinate






	def broadcast_coordinate(self):
		send_data = self.get_basic_status()
		cur_next_coordinate = [[self.local_coordinate[0], self.local_coordinate[1]], \
								[self.local_coordinate[0], self.local_coordinate[1]]]
		send_data['coordinate'] = cur_next_coordinate
		self.network.sendStringData(send_data)

	def walk_one_step(self):
		L2norm = math.sqrt(self.local_direction[0] * self.local_direction[0] + self.local_direction[1] * self.local_direction[1])
		if L2norm != 0:
			self.local_coordinate[0] = self.local_coordinate[0] + self.local_step_size * self.local_direction[0] / L2norm
			self.local_coordinate[1] = self.local_coordinate[1] + self.local_step_size * self.local_direction[1] / L2norm
			core_cmd = "coresendmsg -a %s node number=%s xpos=%s ypos=%s" % (self.controlNet, \
																			self.local_id, \
																			str(int(self.local_coordinate[0])), \
																			str(int(self.local_coordinate[1])))
			# self.local_debugger.send_to_monitor('coordinate: '+ str((int(self.local_coordinate[0]), int(self.local_coordinate[1]))))
			os.system(core_cmd)
			cur_next_coordinate = [[self.local_coordinate[0], self.local_coordinate[1]], \
									[self.local_coordinate[0] + self.local_step_size * self.local_direction[0] / L2norm, \
									 self.local_coordinate[1] + self.local_step_size * self.local_direction[1] / L2norm]]
		else:
			# If direction vector is 0-vector, keep in place
			cur_next_coordinate = [[self.local_coordinate[0], self.local_coordinate[1]], \
									[self.local_coordinate[0], self.local_coordinate[1]]]
			pass
		# Whatever it arrives at the destination, always broadcast coordination to other robots
		send_data = self.get_basic_status()
		send_data['coordinate'] = cur_next_coordinate
		# !! Is here the proper time to clear the global robots' coordinate?
		self.global_robots_coordinate = {}
		self.message_communication(send_data, condition_func=self.check_recv_robots_coordinates, time_out=1)

if __name__ == '__main__':
	index = socket.gethostname()[1:]
	coordinate = [[50,50*i] for i in range(1,21,1)]
	strategy_SRSS = Strategy_SRSS(id=int(index), \
								coordinate=coordinate[int(index)-1], \
								direction=[1, 3], \
								step_size=10, \
								go_interval=0.2, \
								num_robots=20, \
								controlNet='172.16.0.254')
	while True:
		strategy_SRSS.go()




