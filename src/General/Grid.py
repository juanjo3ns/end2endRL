from IPython import embed
from random import randint, choice, random
import numpy as np

class Grid:
	def __init__(self, data):

		self.alg = data['alg']
		self.po = data['po']

		# REWARDS
		self.normal_reward = data['normal_reward']
		self.min_wall = data['min_wall']
		self.max_wall = data['max_wall']
		self.done_reward = data['done_reward']
		self.edge_value = data['edge_value']
		if self.po:
			self.edge_value = -10*data['health']

		# GRID
		self.height = data['width']
		self.width = data['height']
		self.numwalls = data['numwalls']

		self.visibleRad = data['visibleRad']
		self.padded_x = self.height +2*self.visibleRad
		self.padded_y = self.width +2*self.visibleRad
		self.grid = np.zeros((self.padded_x, self.padded_y))
		if data['alg']=="PGM" or data['alg']=="A2C":
			self.walls = []
			self.finalstate = []
			self.initstate = [int(self.padded_x/2), int(self.padded_y/2)]
			self.walls_values = []
		else:
			self.walls = self.formatWalls(data['walls'])
			self.finalstate = self.formatStates(data['finalstate'])
			self.initstate = self.formatStates(data['initstate'])
			self.walls_values = data['walls_values']


	def formatWalls(self, walls):
		for w in walls:
			w[0]+=self.visibleRad
			w[1]+=self.visibleRad
		return walls
	def formatStates(self, state):
		state[0]+=self.visibleRad
		state[1]+=self.visibleRad
		return state

	def reset(self):
		self.grid = np.zeros((self.padded_x, self.padded_y))
		if not self.visibleRad==0:
			self.grid[0:self.visibleRad, :] = self.edge_value
			self.grid[-1*self.visibleRad:, :] = self.edge_value
			self.grid[:, 0:self.visibleRad] = self.edge_value
			self.grid[:, -1*self.visibleRad:] = self.edge_value
		self.setFinalState()
		self.setWalls()


	def setFinalState(self):
		if self.alg == 'PGM' or self.alg == 'A2C':
			final_state = choice([(self.visibleRad, self.visibleRad),
			 	(self.visibleRad,self.padded_y-self.visibleRad-1),
				(self.padded_x-self.visibleRad-1, self.visibleRad),
				(self.padded_x-self.visibleRad-1,self.padded_y-self.visibleRad-1)])
			self.finalstate = final_state
		self.grid[self.finalstate[0],self.finalstate[1]] = self.done_reward

	def setWalls(self):
		if self.alg == 'PGM' or self.alg == 'A2C':
			self.walls.clear()
			self.walls_values.clear()
			for i in range(self.numwalls):
				pos = [randint(self.visibleRad, self.padded_x-self.visibleRad-1),
						randint(self.visibleRad, self.padded_x-self.visibleRad-1)]
				if not pos == self.initstate and not pos == list(self.finalstate):
					value = random()*(self.max_wall-self.min_wall) + self.min_wall
					self.grid[pos[0], pos[1]] = value
					self.walls.append(pos)
					self.walls_values.append(value)
		else:
			for i, w in enumerate(self.walls):
				self.grid[w[0],w[1]] = self.walls_values[i]

	def getEnvironment(self, pos):
		x,y = pos
		if self.po:
			return self.grid[x-self.visibleRad:x+self.visibleRad+1, y-self.visibleRad:y+self.visibleRad+1]
		else:
			walls = np.copy(self.grid)
			finalState = np.zeros_like(self.grid)
			agent = np.zeros_like(self.grid)
			agent[x,y]=1
			index = np.where(self.grid==self.done_reward)
			for i in range(len(index[0])):
				finalState[index[0][i], index[1][i]] = self.done_reward
				walls[index[0][i], index[1][i]] = 0
			return np.stack((walls, finalState, agent))
