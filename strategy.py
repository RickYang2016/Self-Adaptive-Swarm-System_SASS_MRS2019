#!/usr/bin/env python3

#Author: Zhiwei Luo

from task import Strategy, NetworkInterface
import time

class Strategy_SRSS(Strategy):
	mouse = None
	network = None

	local_id = 0
	local_task_id = 0
	local_task_duration = 0
	local_energy_level = 100
	local_round = 0
	local_stage = 'end'
	local_step = 0
	local_negotiation = 0
	local_queue = []					# [3, 1, 2] means the priority: robot-3 > robot-1 > robot-2	
	local_negotiation_result = False	# If all the queues are the same, set as True, otherwise, False

	global_num_robots = 1
	global_num_tasks = 1
	global_energy_level = {}			# {'1': 100, '2':99, '3':85, ...}
	global_negotiation_queue = {}		# {'1': [3, 1, 2], '2': [3, 2, 1], '3': [3, 1, 2], ...}
	global_agreement = {}				# {'1': True, '2': False, '3': True, ...}

	def __init__(self, mouse):
		self.mouse = mouse
		self.network = NetworkInterface()
		self.network.initSocket()
		self.network.startReceiveThread()

	def checkFinished(self):
		return False

	def go(self):
		while True:
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
				continue
				# default stage is 'end'
				# if new tasks are released: local_stage -> 'start'
			else:
				print('Unknown state.')
		sleep(0.5)

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
		time_start = time.time()
		while True:
			self.network.sendStringData(send_data)
			while time.time() - time_start < time_out:
				try:
					recv_data = self.network.retrieveData()
					# if new task is released
					global_condition_func(recv_data)
					if condition_func(recv_data) == True:
						return recv_data
					else
						continue
				except Exception as e:
					pass
				
	def get_basic_status(self):
		status_dict = { \
						'id': self.local_id
						'round': self.local_round
						'stage': self.local_stage
						}
		return status_dict

	def selection(self):
		negotiation = 1
		is_negotiation = True
		while is_negotiation:
			negotiation = negotiation + 1
			self.selection_step1()
			is_negotiation = self.selection_step2()
			is_agreement = self.selection_step3(is_negotiation)

	def check_recv_all_energy(self, recv_data):
		try:
			recv_id = recv_data['id']
			self.global_energy_level[recv_id] = recv_data['energy']
			if len(self.global_energy_level) == self.global_num_robots:
				return False
			else:
				return True
		except Exception as e:
			raise e

	def check_recv_all_queue(self, recv_data):
		try:
			recv_id = recv_data['id']
			self.global_negotiation_queue[recv_id] = recv_data['queue']
			if len(self.global_negotiation_queue) == self.global_num_robots:
				return False
			else:
				return True
		except Exception as e:
			raise e

	def check_recv_all_agreement(self, recv_data):
		try:
			recv_id = recv_data['id']
			self.global_agreement[recv_id] = recv_data['end']
			if len(self.global_agreement) == self.global_num_robots:
				return False
			else:
				return True
		except Exception as e:
			raise e

	# Step1: Exchange energy level
	def selection_step1(self):
		send_data = self.get_basic_status()
		send_data['energy'] = self.local_energy_level
		self.message_communication(send_data, condition_func=self.check_recv_all_energy, timeout=10)
		# the results are stored in 'self.global_energy_level'
		# TODO: 
		# 	generate the queue based on energy and put it into 'self.local_queue'
		self.global_energy_level = {}

	# Step2: Exchange priority queue
	def selection_step2(self):
		send_data = self.get_basic_status()
		send_data['queue'] = self.local_queue
		self.message_communication(send_data, condition_func=self.check_recv_all_queue, timeout=10)
		# the results are stored in 'self.global_negotiation_queue'
		# TODO: 
		# 	compare the queue and put it into 'self.local_negotiation_result'
		self.global_negotiation_queue = {}
		return is_negotiation

	# Step3: Agreement
	def selection_step3(self):
		send_data = self.get_basic_status()
		send_data['end'] = self.local_negotiation_result
		self.message_communication(send_data, condition_func=self.check_recv_all_agreement, timeout=10)
		# the results are stored in 'self.global_agreement'
		# TODO: 
		# 	Check if all the agreement results are 'True', set is_agreement = True / False
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