#!/usr/bin/env python3

#Author: Zhiwei Luo

from task import Strategy, NetworkInterface
from time import sleep
from numpy import np

class StrategyTestProgress(Strategy):
	progress = 10

	def checkFinished(self):
		return self.progress <= 0

	def go(self):
		self.progress = self.progress - 1
		print(self.progress)

class StrategyTestCount(Strategy):
	progress = 0

	def checkFinished(self):
		return self.progress > 10

	def go(self):
		self.progress = self.progress + 1
		print(self.progress)
		sleep(1)

class StrategyTestGoDown(Strategy):
	mouse = None
	mapPainter = None
	progress = 0

	def __init__(self, mouse, mapPainter):
		self.mouse = mouse
		self.mapPainter = mapPainter

	def checkFinished(self):
		return self.progress >= 1

	def go(self):
		self.progress = self.progress + 1
		print(self.progress)
		sleep(1)
		self.mouse.goDown()
		self.mouse.goDown()
		self.mouse.goDown()
		self.mouse.goDown()
		self.mouse.goRight()
		self.mouse.goUp()
		cell = self.mouse.mazeMap.getCell(self.mouse.x, self.mouse.y)
		self.mapPainter.putRobotInCell(cell)
		sleep(1)
		

class StrategyTestDFS(Strategy):
	mouse = None
	mapPainter = None
	isVisited = []
	path = []
	isBack = False

	def __init__(self, mouse, mapPainter):
		self.mouse = mouse
		self.mapPainter = mapPainter
		self.isVisited = [[0 for i in range(self.mouse.mazeMap.width)] for j in range(self.mouse.mazeMap.height)]
		self.isVisited[self.mouse.x][self.mouse.y] = 1

	def checkFinished(self):
		return self.isBack

	def go(self):
		cell = self.mouse.mazeMap.getCell(self.mouse.x, self.mouse.y)
		self.mapPainter.drawCell(cell, 'grey')

		if self.mouse.canGoLeft() and not self.isVisited[self.mouse.x-1][self.mouse.y]:
			self.path.append([self.mouse.x, self.mouse.y])
			self.isVisited[self.mouse.x-1][self.mouse.y] = 1
			self.mouse.goLeft()
		elif self.mouse.canGoUp() and not self.isVisited[self.mouse.x][self.mouse.y-1]:
			self.path.append([self.mouse.x, self.mouse.y])
			self.isVisited[self.mouse.x][self.mouse.y-1] = 1
			self.mouse.goUp()
		elif self.mouse.canGoRight() and not self.isVisited[self.mouse.x+1][self.mouse.y]:
			self.path.append([self.mouse.x, self.mouse.y])
			self.isVisited[self.mouse.x+1][self.mouse.y] = 1
			self.mouse.goRight()
		elif self.mouse.canGoDown() and not self.isVisited[self.mouse.x][self.mouse.y+1]:
			self.path.append([self.mouse.x, self.mouse.y])
			self.isVisited[self.mouse.x][self.mouse.y+1] = 1
			self.mouse.goDown()
		else:
			if len(self.path) != 0:
				x, y = self.path.pop()
				if x < self.mouse.x:
					self.mouse.goLeft()
				elif x > self.mouse.x:
					self.mouse.goRight()
				elif y < self.mouse.y:
					self.mouse.goUp()
				elif y > self.mouse.y:
					self.mouse.goDown()
			else:
				self.isBack = True

		cell = self.mouse.mazeMap.getCell(self.mouse.x, self.mouse.y)
		self.mapPainter.putRobotInCell(cell)
		sleep(0.05)


# ============================================================================================================


#input: the sorted priority queue and all the robots' energy level
#output: the robot specifical task's id
def Selection(q):
		# we define each robot having an energy level ei, according to the energy level we can partition them into different groups relative evenly.

		for i in n:
			p[i] = p[i-1] + e[i]
		
		for i in n:
			M[i, 1] = p[i]

		for i in k:
			M[1, j] = e1

		for i in xrange(1, n):

			for m in xrange(1, k):
				M[] = -1

				for j in range(i):
					s = min( max( M[], sum() ) )
		

#input: the task position, and the sorted priority queue
#output: the robot specifical goal point
def Formation(q, tx, ty):
	sep = (2 * math.pi) / n
	    for x in n:
	        theta = x * sep
	        yield (task.position[0] + task.radius * math.cos(theta),
				   task.position[1] + task.radius * math.sin(theta))

#input: the task position, and the sorted priority queue
#output: the robot_i's routing plan and next step behavior
def Routing(q):
	for j in range(len(q)):
		if q[i].direction == q[j].direction && i > j:
			q[i].direction = q[i].direction + 10

	while(q != NULL)
	{
		r == q.pop()
		if q[i].id == r:
			robot.move()
		else
			robot.stop()
	}

#input: the unsorted priority qi
#output: the sorted priority qi
def Selecting Plan Negotiation():
	pass

#input: the unsorted priority qi
#output: the sorted priority qi
def Formation Plan Negotiation():
	pass

#input: the unsorted priority qi
#output: the sorted priority qi
def Routing Plan Negotiation(q):
	sorted(d.keys())

	while( d[i].keys() == d[j].keys() )
	{
		sorted( d[i].items(), key = lambda item:item[1] )
	}

#input: the sorted priority qj
#output: excute the plan or negotiate again
def Selection Agreement(q):
	pass

#input: the sorted priority qj
#output: excute the plan or negotiate again
def Formation Agreement(q):
	pass

#input: the sorted priority qj
#output: excute the plan or negotiate again
def Routing Agreement(q):
	pass

	def get_cross(p1, p2, p):

			return (p2.x - p1.x) * (p.y - p1.y) -(p.x - p1.x) * (p2.y - p1.y)




	def collision_detect(self):

		p = [0]

		direction = math.atan(self.local_coordinate[1]/self.local_coordinate[0])

		plu_x = self.local_coordinate[0] + math.sqrt(2) * self.local_robot_radius * math.cos(direction + math.pi / 4)
		plu_y = self.local_coordinate[1] + math.sqrt(2) * self.local_robot_radius * math.sin(direction + math.pi / 4)
		pld_x = self.local_coordinate[0] + math.sqrt(2) * self.local_robot_radius * math.cos(direction - math.pi / 4)
		pld_y = self.local_coordinate[1] + math.sqrt(2) * self.local_robot_radius * math.sin(direction - math.pi / 4)
		pru_x = plu_x + self.local_step_size * math.cos(direction)
		pru_y = plu_y + self.local_step_size * math.sin(direction)
		prd_x = pld_x + self.local_step_size * math.cos(direction)
		prd_y = pld_y + self.local_step_size * math.sin(direction)

		for i in range(len(self.global_robots_coordinate)):
			if get_cross(plu, pld, self.global_robots_coordinate[i]) * get_cross(pru, prd, self.global_robots_coordinate[i]) >= 0 && 
			   get_cross(pld, pru, self.global_robots_coordinate[i]) * get_cross(prd, plu, self.global_robots_coordinate[i]) >= 0 :
			   	p = self.global_robots_coordinate[i]

	def routing_execution(self):
		# n = len(self.global_energy_level)

		for i in range(len(p)):
			theta = atan(2 * self.local_robot_radius / (math.sqrt(math.pow(self.local_coordinate[0] - p[i][0], 2) 
				+ math.pow(self.local_coordinate[1] - p[i][1], 2)) - self.local_robot_radius * 2))

			relative_direction = p - self.local_direction

			theta1 = acos(self.local_direction * relative_direction / math.sqrt(math.pow(self.local_coordinate[0], 2) + math.pow(self.local_coordinate[1], 2)) *
				math.sqrt(math.pow(relative_direction[0], 2) + math.pow(relative_direction[1], 2))
 			
 			update_angle = atan(self.local_direction[1]/self.local_direction[0])

			if theta1 <= theta && self.local_id == i:
				update_angle = aten(self.local_direction[1]/self.local_direction[0]) + theta - theta1

