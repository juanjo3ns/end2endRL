from IPython import embed
from random import randint, choice, random
import numpy as np

'''
In this script we define the class grid that basically returns the board filled
with walls, paddings and final states.
The interesting thing is that we can select among different environments with the
parameter 'env'.
From 0 to 5 are hardcoded environments where the wall value is -1 and the
positions are predefined.
From 6 to 10 the environment's walls have random positions and values.
In the particular case of env 9 and 10, the wall's positon and values
changes every episode. The final state also changes among 4 possible states.
'''

class Grid:
	def __init__(self,
		height=10,
		width=10,
		env=0,
		po=False,
		visibleRad=1):

		self.env = env
		self.po = po

		# REWARDS
		self.normal_reward = -0.04
		self.min_wall = -1
		self.max_wall = 0
		self.done_reward = 10
		self.edge_value = -1
		if self.po:
			self.max_wall = 0.5
			self.edge_value = -10

		# GRID
		self.height = height
		self.width = width
		self.numWalls = int(height*width/4)
		# self.numWalls = 0
		self.visibleRad = visibleRad
		self.padded_x = self.height +2*self.visibleRad
		self.padded_y = self.width +2*self.visibleRad
		self.grid = np.zeros((self.padded_x, self.padded_y))
		self.saved_walls = []
		self.saved_values = []

	def reset(self):
		self.grid = np.zeros((self.padded_x, self.padded_y))
		if not self.visibleRad==0:
			self.grid[0:self.visibleRad, :] = self.edge_value
			self.grid[-1*self.visibleRad:, :] = self.edge_value
			self.grid[:, 0:self.visibleRad] = self.edge_value
			self.grid[:, -1*self.visibleRad:] = self.edge_value
		self.setWalls()
		self.setFinalState()

	def generateEnv8(self):
		gwalls = []
		alternate = 0
		for i in range(self.padded_x):
			walls = []
			if i%2==0 and i>0 and i<(self.padded_x-self.visibleRad-1):
				if alternate%4==0:
					for j in list(range(self.padded_y))[2:]:
						if j<(self.padded_y-self.visibleRad):
							walls.append([i,j])
				else:
					for j in list(range(self.padded_y))[:-2]:
						if j>0:
							walls.append([i,j])
			gwalls.extend(walls)
			alternate += 1
		return gwalls

	def setWalls(self):
		# WALLS OF DIFFERENT ENVIRONMENTS

		# Walls positions
		self.walls = {
		0: ([[3, i] for i in range(4,self.width+1)],[[7, i] for i in range(self.visibleRad,self.width-3)]),
		1: ([[i, 4] for i in range(4,self.height)],[[i, 5] for i in range(4,self.height)]),
		2: ([[[i, 4] for i in range(4,self.height-1)]]),
		3: ([[[i, 4] for i in range(0,self.height-1)]]),
		4: ([[]]),
		5: ([[3, i] for i in range(0,4)],
			[[3, i] for i in range(5,self.width)],
			[[i, 3] for i in range(1, 3)],
			[[i, 5] for i in range(1, 3)],
			[[i, j] for i in range(0, 3) for j in range(0,3)],
			[[i, j] for i in range(0, 3) for j in range(6, self.width)]),
		6: (lambda: (randint(self.visibleRad,self.padded_x-self.visibleRad-2),randint(self.visibleRad,self.padded_y-self.visibleRad-1))),
		7: (lambda: (randint(self.visibleRad,self.padded_x-self.visibleRad-1),randint(self.visibleRad,self.padded_y-self.visibleRad-1))),
		8: (lambda: self.generateEnv8())
		}

		# Walls values
		self.walls_values = {
		0: -1, 1: -1,3: -1,4: -1, 5: -1,
		6: (lambda: random()*(self.max_wall-self.min_wall) + self.min_wall),
		7: (lambda: random()*(self.max_wall-self.min_wall) + self.min_wall),
		8: -1
		}

		# Walls update
		self.walls_updates = {0:0, 1:0, 3:0, 4:0, 5:0, 6:0, 7:1, 8:0 }

		walls = []
		if self.env > 5:
			if self.env==8:
				func = self.walls[self.env]
				walls.extend(func())
			else:
				for i in range(self.numWalls):
					random_wall = self.walls[self.env]
					w = random_wall()
					if not w in walls:
						walls.append(list(random_wall()))
			if len(self.saved_walls)==0 or self.walls_updates[self.env]:
				# In the case we update walls and values, clear list
				self.saved_walls.clear()
				self.saved_values.clear()
				for i in walls:
					value = self.walls_values[self.env]
					if not type(value)==int:
						value = value()
					self.saved_walls.append(i)
					self.saved_values.append(value)
					self.grid[i[0],i[1]] = value
				# print(self.grid.round(1))
			else:
				for i,value in zip(self.saved_walls,self.saved_values):
					self.grid[i[0],i[1]] = value
		else:
			for w in self.walls[self.env]:
				for i in w:
					walls.append(i)
					self.grid[i[0],i[1]] = -1

	def setFinalState(self):
		# FINAL STATES OF DIFFERENT ENVIORONMENTS
		self.finalState = {
		0: ([[self.height-1,0]]),
		1: ([[self.height-1,0]]),
		2: ([[int((self.height-1)/2),0]]),
		3: ([[int((self.height-1)/2),0]]),
		4: ([[int((self.height-1)/2),0]]),
		5: ([[0,3],[0,5]]),
		6: ([[self.padded_x - self.visibleRad - 1,int((self.padded_y-1)/2)]]),
		7: ([choice([(self.visibleRad, self.visibleRad),
		 	(self.visibleRad,self.padded_y-self.visibleRad-1),
			(self.padded_x-self.visibleRad-1, self.visibleRad),
			(self.padded_x-self.visibleRad-1,self.padded_y-self.visibleRad-1)])]),
		8: ([[self.padded_x-self.visibleRad-1,self.padded_y-self.visibleRad-1]]),
		}
		for i in self.finalState[self.env]:
			if list(i) in self.saved_walls:
				index = self.saved_walls.index(list(i))
				self.saved_walls.remove(self.saved_walls[index])
				self.saved_values.remove(self.saved_values[index])
			self.grid[i[0],i[1]] = self.done_reward


	def getInitState(self, random):
		# INIT STATES OF DIFFERENT ENVIRONMENTS
		self.initState = {
		0: ([0,self.width-1]),
		1: ([self.height-1,self.width-1]),
		2: ([self.height-1,self.width-1]),
		3: ([self.height-1,self.width-1]),
		4: ([self.height-1,self.width-1]),
		5: ([self.height-1,2]),
		6: ([self.visibleRad,int((self.padded_y-1)/2)]),
		7: ([int(self.padded_x/2),int(self.padded_y/2)]),
		8: ([self.visibleRad,self.visibleRad])
		}
		if random:
			return (randint(self.visibleRad,self.padded_x-self.visibleRad-1),randint(self.visibleRad,self.padded_y-self.visibleRad-1))
		return self.initState[self.env]


	def getEnvironment(self, pos):
		x,y = pos
		if self.po:
			return self.grid[x-self.visibleRad:x+self.visibleRad+1, y-self.visibleRad:y+self.visibleRad+1]
		else:
			# grid = self.grid.copy()
			# grid[x,y]=1
			# return grid[self.visibleRad:-self.visibleRad,self.visibleRad:-self.visibleRad]
			walls = np.copy(self.grid)
			finalState = np.zeros_like(self.grid)
			agent = np.zeros_like(self.grid)
			agent[x,y]=1
			index = np.where(self.grid==10)
			for i in range(len(index[0])):
				finalState[index[0][i], index[1][i]] = 1
				walls[index[0][i], index[1][i]] = 0
			return np.stack((walls, finalState, agent))


# g = Grid(height=10, width=10, env=0, po=False, visibleRad=0)
# g.reset()
# print(g.grid)
# print(g.getEnvironment((1,1)))
# print(g.getEnvironment((5,5)))
# g = Grid(height=6, width=6, env=9, po=True, visibleRad=1)
# g.reset()
# print(g.grid)
# print(g.getEnvironment((1,1)))
# print(g.getEnvironment((5,5)))
# embed()
