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
def Formation Agreement():
	pass

#input: the sorted priority qj
#output: excute the plan or negotiate again
def Routing Agreement():
	pass


# ================================================================================================================


class StrategyMultiTasks(Strategy):
	mouse = None
	isVisited = []
	path = []
	isBack = False
	network = None
	rounds = 0

	def __init__(self, mouse):
		self.mouse = mouse
		self.isVisited = [[0 for i in range(self.mouse.mazeMap.width)] for j in range(self.mouse.mazeMap.height)]
		self.isVisited[self.mouse.x][self.mouse.y] = 1
		self.network = NetworkInterface()
		self.network.initSocket()
		self.network.startReceiveThread()

	def checkFinished(self):
		return self.isBack

	def go(self):
		self.mouse.senseWalls()
		rounds++
		# print(self.mouse.getCurrentCell().getWhichIsWall())
		sendData = {'x': self.mouse.x, 'y':self.mouse.y, 'up': not self.mouse.canGoUp(), 'down': not self.mouse.canGoDown(), 'left': not self.mouse.canGoLeft(), 'right': not self.mouse.canGoRight()
					'id': self.network.myIPAddr, 'rounds': self.rounds }

		self.network.sendStringData(sendData)
		recvData = self.network.retrieveData()
		ui = np.array([0, 0])

		while recvData:
			otherMap = recvData
			cell = self.mouse.mazeMap.getCell(otherMap['x'], otherMap['y'])
			rj = np.array(otherMap['x'], otherMap['y'])


			# self.isVisited[otherMap['x']][otherMap['y']] = 1
			if otherMap['up']: self.mouse.mazeMap.setCellUpAsWall(cell)
			if otherMap['down']: self.mouse.mazeMap.setCellDownAsWall(cell)
			if otherMap['left']: self.mouse.mazeMap.setCellLeftAsWall(cell)
			if otherMap['right']: self.mouse.mazeMap.setCellRightAsWall(cell)
			recvData = self.network.retrieveData()

			if self.rounds == otherMap['rounds']:

				ri = np.array([self.mouse.x, self.mouse.y])

				ui = ui + (ri - rj)

		disUi = np.linalg.norm(ui)

		if ui[1] != 0:
			argUi = np.arctan(ui[0]/ui[1])*180/np.pi
		else
			argUi = 0	

		while disUi != 0 :

			if ( argUi >= 0 and argUi < 45 ) or ( argUi >= 315 and argUi < 360 ):
				if self.mouse.canGoRight():
					self.path.append([self.mouse.x, self.mouse.y])
					self.mouse.goRight()
				elif 0 <= argUi and argUi < 45 and self.mouse.canGoUp():
					self.path.append([self.mouse.x, self.mouse.y])
					self.mouse.goUp()
				elif 315 <= argUi and argUi < 360 and self.mouse.canGoDown():
					self.path.append([self.mouse.x, self.mouse.y])
					self.mouse.goDown()
			elif self.mouse.canGoUp():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goUp()							
			elif self.mouse.canGoDown():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goDown()
			elif self.mouse.canGoLeft():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goLeft()

			if argUi >= 45 and argUi < 135 :
				if self.mouse.canGoUp():
					self.path.append([self.mouse.x, self.mouse.y])
					self.mouse.goUp()
				elif 45 <= argUi and argUi < 90 and self.mouse.canGoRight():
					self.path.append([self.mouse.x, self.mouse.y])
					self.mouse.goRight()
				elif 90 <= argUi and argUi < 135 and self.mouse.canGoLeft():
					self.path.append([self.mouse.x, self.mouse.y])
					self.mouse.goLeft()
			elif self.mouse.canGoLeft():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goLeft()							
			elif self.mouse.canGoRight():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goRight()
			elif self.mouse.canGoDown():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goDown()	

			if argUi >= 135 and argUi < 225:
				if self.mouse.canGoLeft():
					self.path.append([self.mouse.x, self.mouse.y])
					self.mouse.goLeft()
				elif 135 <= argUi and argUi < 180 and self.mouse.canGoUp():
						self.path.append([self.mouse.x, self.mouse.y])
						self.mouse.goUp()											
				elif 180 <= argUi and argUi < 225 and self.mouse.canGoDown():
						self.path.append([self.mouse.x, self.mouse.y])
						self.mouse.goDown()
			elif self.mouse.canGoUp():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goUp()	
			elif self.mouse.canGoDown():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goDown()							
			elif self.mouse.canGoRight():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goRight()

			if argUi >= 225 and argUi < 315:
				if self.mouse.canGoDown():
					self.path.append([self.mouse.x, self.mouse.y])
					self.mouse.goDown()
				elif 225 <= argUi and argUi < 270 and self.mouse.canGoLeft():
					self.path.append([self.mouse.x, self.mouse.y])
					self.mouse.goLeft()
				elif 270 <= argUi and argUi < 315 and self.mouse.canGoRight():
					self.path.append([self.mouse.x, self.mouse.y])
					self.mouse.goRight()
			elif self.mouse.canGoLeft():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goLeft()							
			elif self.mouse.canGoRight():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goRight()
			elif self.mouse.canGoUp():
				self.path.append([self.mouse.x, self.mouse.y])
				self.mouse.goUp()

		# if self.mouse.canGoLeft() and not self.isVisited[self.mouse.x-1][self.mouse.y]:
		# 	self.path.append([self.mouse.x, self.mouse.y])
		# 	self.isVisited[self.mouse.x-1][self.mouse.y] = 1
		# 	self.mouse.goLeft()
		# elif self.mouse.canGoUp() and not self.isVisited[self.mouse.x][self.mouse.y-1]:
		# 	self.path.append([self.mouse.x, self.mouse.y])
		# 	self.isVisited[self.mouse.x][self.mouse.y-1] = 1
		# 	self.mouse.goUp()
		# elif self.mouse.canGoRight() and not self.isVisited[self.mouse.x+1][self.mouse.y]:
		# 	self.path.append([self.mouse.x, self.mouse.y])
		# 	self.isVisited[self.mouse.x+1][self.mouse.y] = 1
		# 	self.mouse.goRight()
		# elif self.mouse.canGoDown() and not self.isVisited[self.mouse.x][self.mouse.y+1]:
		# 	self.path.append([self.mouse.x, self.mouse.y])
		# 	self.isVisited[self.mouse.x][self.mouse.y+1] = 1
		# 	self.mouse.goDown()
		# else:
		# 	if len(self.path) != 0:
		# 		x, y = self.path.pop()
		# 		if x < self.mouse.x:
		# 			self.mouse.goLeft()
		# 		elif x > self.mouse.x:
		# 			self.mouse.goRight()
		# 		elif y < self.mouse.y:
		# 			self.mouse.goUp()
		# 		elif y > self.mouse.y:
		# 			self.mouse.goDown()
		# 	else:
		# 		self.isBack = True

		sleep(0.5)
		

# class StrategyTestMultiDFS(Strategy):
# 	mouse = None
# 	isVisited = []
# 	path = []
# 	isBack = False
# 	network = None

# 	def __init__(self, mouse):
# 		self.mouse = mouse
# 		self.isVisited = [[0 for i in range(self.mouse.mazeMap.width)] for j in range(self.mouse.mazeMap.height)]
# 		self.isVisited[self.mouse.x][self.mouse.y] = 1
# 		self.network = NetworkInterface()
# 		self.network.initSocket()
# 		self.network.startReceiveThread()

# 	def checkFinished(self):
# 		return self.isBack

# 	def go(self):
# 		self.mouse.senseWalls()
# 		print(self.mouse.getCurrentCell().getWhichIsWall())
# 		sendData = {'x': self.mouse.x, 'y':self.mouse.y, 'up': not self.mouse.canGoUp(), 'down': not self.mouse.canGoDown(), 'left': not self.mouse.canGoLeft(), 'right': not self.mouse.canGoRight()
# 					'id': self.network.myIPAddr}
# 		self.network.sendStringData(sendData)
# 		recvData = self.network.retrieveData()
# 		while recvData:
# 			otherMap = recvData
# 			cell = self.mouse.mazeMap.getCell(otherMap['x'], otherMap['y'])
# 			self.isVisited[otherMap['x']][otherMap['y']] = 1
# 			if otherMap['up']: self.mouse.mazeMap.setCellUpAsWall(cell)
# 			if otherMap['down']: self.mouse.mazeMap.setCellDownAsWall(cell)
# 			if otherMap['left']: self.mouse.mazeMap.setCellLeftAsWall(cell)
# 			if otherMap['right']: self.mouse.mazeMap.setCellRightAsWall(cell)
# 			recvData = self.network.retrieveData()

# 		if self.mouse.canGoLeft() and not self.isVisited[self.mouse.x-1][self.mouse.y]:
# 			self.path.append([self.mouse.x, self.mouse.y])
# 			self.isVisited[self.mouse.x-1][self.mouse.y] = 1
# 			self.mouse.goLeft()
# 		elif self.mouse.canGoUp() and not self.isVisited[self.mouse.x][self.mouse.y-1]:
# 			self.path.append([self.mouse.x, self.mouse.y])
# 			self.isVisited[self.mouse.x][self.mouse.y-1] = 1
# 			self.mouse.goUp()
# 		elif self.mouse.canGoRight() and not self.isVisited[self.mouse.x+1][self.mouse.y]:
# 			self.path.append([self.mouse.x, self.mouse.y])
# 			self.isVisited[self.mouse.x+1][self.mouse.y] = 1
# 			self.mouse.goRight()
# 		elif self.mouse.canGoDown() and not self.isVisited[self.mouse.x][self.mouse.y+1]:
# 			self.path.append([self.mouse.x, self.mouse.y])
# 			self.isVisited[self.mouse.x][self.mouse.y+1] = 1
# 			self.mouse.goDown()
# 		else:
# 			if len(self.path) != 0:
# 				x, y = self.path.pop()
# 				if x < self.mouse.x:
# 					self.mouse.goLeft()
# 				elif x > self.mouse.x:
# 					self.mouse.goRight()
# 				elif y < self.mouse.y:
# 					self.mouse.goUp()
# 				elif y > self.mouse.y:
# 					self.mouse.goDown()
# 			else:
# 				self.isBack = True

# 		sleep(0.5)


class StrategyTestDFSEV3(Strategy):
	mouse = None
	#mapPainter = None
	isVisited = []
	path = []
	isBack = False

	def __init__(self, mouse):
		self.mouse = mouse
		#self.mapPainter = mapPainter
		self.isVisited = [[0 for i in range(self.mouse.mazeMap.width)] for j in range(self.mouse.mazeMap.height)]
		self.isVisited[self.mouse.x][self.mouse.y] = 1

	def checkFinished(self):
		return self.isBack

	def go(self):
		#cell = self.mouse.mazeMap.getCell(self.mouse.x, self.mouse.y)
		#self.mapPainter.drawCell(cell, 'grey')
		self.mouse.senseWalls()
		print(self.mouse.getCurrentCell().getWhichIsWall())

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

		#cell = self.mouse.mazeMap.getCell(self.mouse.x, self.mouse.y)
		#self.mapPainter.putRobotInCell(cell)

class StrategyTestGoStepEV3(Strategy):
	mouse = None
	progress = 0

	def __init__(self, mouse):
		self.mouse = mouse

	def checkFinished(self):
		return self.progress >= 1

	def go(self):
		self.progress = self.progress + 1
		self.mouse.senseWalls()
		print(self.mouse.getCurrentCell().getWhichIsWall())
		self.mouse.goLeft()
		self.mouse.senseWalls()
		print(self.mouse.getCurrentCell().getWhichIsWall())
		self.mouse.goRight()
		self.mouse.senseWalls()
		print(self.mouse.getCurrentCell().getWhichIsWall())
		self.mouse.goUp()
		self.mouse.senseWalls()
		print(self.mouse.getCurrentCell().getWhichIsWall())
		self.mouse.goDown()
		self.mouse.senseWalls()
		print(self.mouse.getCurrentCell().getWhichIsWall())
		sleep(1)

class StrategyTestInitEV3(Strategy):
	mouse = None
	flag = False

	def __init__(self, mouse):
		self.mouse = mouse

	def checkFinished(self):
		return self.flag

	def go(self):
		self.mouse.commandTranslator.motorController.gyreset()
		self.flag = True
		sleep(1)

class StrategyTestDFSDisplayEV3(Strategy):
	mouse = None
	isVisited = []
	path = []
	isBack = False

	def __init__(self, mouse):
		self.mouse = mouse
		self.isVisited = [[0 for i in range(self.mouse.mazeMap.width)] for j in range(self.mouse.mazeMap.height)]
		self.isVisited[self.mouse.x][self.mouse.y] = 1
		self.network = NetworkInterface()
		self.network.initSocket()

	def checkFinished(self):
		return self.isBack

	def go(self):
		self.mouse.senseWalls()
		print(self.mouse.getCurrentCell().getWhichIsWall())
		sendData = {'x': self.mouse.x, 'y':self.mouse.y, 'up':self.mouse.canGoUp(), 'down':self.mouse.canGoDown(), 'left':self.mouse.canGoLeft(), 'right':self.mouse.canGoRight()}
		self.network.sendStringData(sendData)

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
