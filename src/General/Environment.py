import os
import numpy as np
import random
import torch
from tqdm import tqdm
from IPython import embed
from collections import defaultdict
from random import choice

from src.DQN.newDDQN import DDQN
from src.GA.ga import GA
from src.PGM.reinforce import Reinforce
from src.PGM.actorcritic import ActorCritic

from src.General.Agent import Agent
from src.General.Grid import Grid

from src.utils.writecsv import CSV
from src.utils.plot import *

from tensorboardX import SummaryWriter


class Environment:
	def __init__(self,
				 grid,
				 eps_scheduled=0,
				 height=10,
				 width=3,
				 numAgents=2,
				 health=1,
				 po=False,
				 visibleRad=1,
				 alg="DQN",
				 tbX=False,
				 save=False,
				 save_freq=10,
				 batch_size=1000,
				 iterations=4000,
				 sigma=0.02,
				 pos=0.05,
				 version='0.0.0'):

		# GLOBAL PARAMETERS
		self.newGeneralMovements = 0
		self.iterations = iterations
		self.actions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

		# CUSTOMIZABLE PARAMETERS
		# - TENSORBOARD AND WEIGHTS PARAMETERS
		self.tbX = tbX
		self.version = version
		self.save = save
		self.save_freq = save_freq
		# - ENVIRONMENT PARAMETERS
		self.po = po
		self.visibleRad= visibleRad
		self.alg = alg
		self.eps_scheduled=eps_scheduled
		self.numAgents = numAgents
		self.height = height
		self.width = width
		self.sigma = sigma
		self.pos = pos


		# ENVIRONMENT
		self.grid = grid

		self.agents = defaultdict(
						lambda: Agent(height = self.height,
									 width = self.width,
									 alg=self.alg,
									 visibleRad=self.visibleRad,
									 health=health,
									 batch_size=batch_size,
									 po=self.po))


		# TENSORBOARD X
		if self.tbX:
			self.writer = SummaryWriter(os.path.join("../src/tensorboard",self.alg,self.version))
		# INITIALIZE AGENTS
		self.initAgents()

		# ALGORITHMS SCRIPTS
		self.reinforce = Reinforce()
		self.ddqn = DDQN()
		self.ga = GA(self.agents, self.sigma, self.pos)
		self.a2c = ActorCritic()

		# CSV WRITERS
		self.csv_coords = None
		self.csv_info = None

		# PATHS
		self.weights_path = '/data/src/weights/'


	def addFigs(self, it, agent, freq):
		if it%freq==0:
			base = np.zeros_like(self.grid.grid)
			v = self.grid.visibleRad
			base = base[v:-v,v:-v]
			q_values = np.zeros_like(base)
			x = np.zeros_like(base)
			y = np.zeros_like(base)
			for i in range(0,self.grid.padded_x-self.grid.visibleRad*2):
				for j in range(0,self.grid.padded_y-self.grid.visibleRad*2):
					env = self.grid.getEnvironment((i,j)).astype(np.float32)
					output = agent.forward(env)
					directions = output[0].cpu().numpy()
					x[i,j] = directions[0]-directions[1]
					y[i,j] = directions[3]-directions[2]

					q_values[i,j] = output.max(1)[0][0]
			fig1 = values(q_values)
			fig2 = arrows(x,y)
			self.writer.add_figure("V values", fig1, global_step=it)
			self.writer.add_figure("Directions", fig2, global_step=it)

	# TENSORBOARD LOGS AND SAVE MODEL WEIGHTS
	def logs(self, it):
		if self.tbX:
			if self.alg=="DQN":
				self.writer.add_scalar('Loss', self.agents[0].loss, it)
				self.writer.add_scalar('Movements', self.agents[0].movements, it)
				self.writer.add_scalar('Health', self.agents[0].health, it)
				self.writer.add_scalar('Reward', self.agents[0].totalreward, it)
				self.writer.add_scalar('Epsilon', self.getEps(it), it)
				# self.writer.add_scalar('Fruits', self.agents[0].fruits, it)
				self.addFigs(it, self.agents[0], 2000)
			elif self.alg=="GA":
				h = []
				won=0
				for n in range(self.numAgents):
					agent = self.agents[n]
					if agent.won:
						if won==0: # We only want to show the q-values of one agent, we pick the first that wins
							self.addFigs(it, self.agents[n], 50)
						won +=1
				for n in self.ga.elite:
					h.append(self.agents[n].totalreward)
				if won==0: # If any agent has won we pick the first one from the elite
					self.addFigs(it, self.agents[self.ga.elite[0]], 50)
				avg = sum(h)/len(h)
				self.writer.add_scalar('Reward', avg, self.ga.mutation)
				self.writer.add_scalar('Variance', self.ga.sigma, self.ga.mutation)
				self.writer.add_scalar('Survivals', won/self.ga.numAgents, self.ga.mutation)
				self.writer.add_scalar('Epsilon', self.getEps(it), self.ga.mutation)
			elif self.alg=="PGM" or self.alg=="A2C":
				self.writer.add_scalar('Fruits', self.agents[0].fruits, it)
				self.writer.add_scalar('Loss', self.agents[0].loss, it)
				self.writer.add_scalar('Movements', self.agents[0].movements, it)
				self.writer.add_scalar('Health', self.agents[0].health, it)
				self.writer.add_scalar('Reward', self.agents[0].totalreward, it)
		if it%self.save_freq==0 and self.save:
			if self.alg=="GA":
				for i,e in enumerate(self.ga.elite):
					self.agents[e].saveModel(self.version, i, int(it/self.save_freq))

			else:
				for n in range(self.numAgents):
					self.agents[n].saveModel(self.version, n, int(it/self.save_freq))

	# RESET COMMON STUFF LIKE AGENTS OR GRID
	def reset(self):
		self.initAgents()
		self.grid.reset()
		self.newGeneralMovements = 0
		self.ga.reset()

	# RESET EACH AGENT
	def initAgents(self):
		for n in range(self.numAgents):
			self.agents[n].reset(self.grid.initstate)

	# RETURN EPSILON DEPENDING ON ITERATION
	def getEps(self,it):
		return self.eps_scheduled(it)


	# SELECT ACTION FOR DQN AND GA
	def selectAction(self,output,it, agent):
		if random.random() > self.getEps(it) and it > agent.start_learning:
			# print(self.actions[output.max(1)[1][0]],output)
			return self.actions[output.max(1)[1][0]]

		return self.actions[np.random.choice(range(len(self.actions)))]

	# ONE STEP FOR EACH AGENT
	def step(self,it):
		for n in range(self.numAgents):
			agent = self.agents[n]
			if not agent.done:
				env = self.grid.getEnvironment(agent.state).astype(np.float32)
				output = agent.forward(env,it)
				# DOUBLE DQN
				if self.alg=="DQN":
					action = self.selectAction(output, it, agent)
					reward = self.takeAction(agent, action)
					agent.buffer.store((agent.prev_state, self.actions.index(action), agent.state, reward, 0 if agent.won else 1))

				# GENETIC ALGORITHMS
				elif self.alg=="GA":
					action = self.selectAction(output, it, agent)
					reward = self.takeActionGA(agent, action)

				# REINFORCE WITH BASELINE
				elif self.alg=="PGM":
					action, log_action, value = self.reinforce.selectAction(output)
					reward = self.takeAction(agent, self.actions[int(action)])
					self.reinforce.append(agent, value, log_action, reward)

				# ACTOR CRITIC
				elif self.alg=="A2C":
					action = self.a2c.selectAction(output)
					reward = self.takeAction(agent, self.actions[int(action)])
					next_env = self.grid.getEnvironment(agent.state).astype(np.float32)
					self.a2c.actorcritic(agent, reward, next_env)

	'''	PARTICULAR FUNCTIONS FOR EACH DIFFERENT ALGORITHM'''
	def env_reinforce(self):
		for n in range(self.numAgents):
			agent = self.agents[n]
			return self.reinforce.reinforce(agent)

	def env_geneticalgorithms(self, it):
		self.ga.selectElite()
		self.ga.generateNewAgents()
		won=0
		for n in range(self.numAgents):
			agent = self.agents[n]
			if agent.won:
				won+=1
		print("Variance {} #{} agents achieved final state in mutation {}".format(round(self.ga.sigma,3), won, self.ga.mutation))
		# if it % 10 == 0:
		self.ga.updateVariance(won)


	def env_dqn(self, it):
		self.grid.reset()
		for n in range(self.numAgents):
			agent = self.agents[n]
			if it > agent.start_learning:
				sample_data = agent.buffer.sample()
				states = np.array([self.grid.getEnvironment(x).astype(np.float32) for x in sample_data['state']])
				next_states = np.array([self.grid.getEnvironment(x).astype(np.float32) for x in sample_data['next_state']])
				actions = np.array(sample_data['action'])
				rewards = np.array(sample_data['reward'])
				dones = np.array(sample_data['done'])
				self.ddqn.train(agent, states, next_states, actions, rewards, dones)
				if it % agent.target_update_freq == 0:
					agent.updateTargetNN()
	'''--------------------------------------------------'''
	def nextState(self, agent, action):
		nextState = np.array(agent.state) + np.array(action)
		if -1 in nextState or self.grid.padded_x == nextState[0] or self.grid.padded_y == nextState[1]:
			nextState = agent.state
		return nextState
	# GENERIC FUNCTION FOR ALL THE DIFFERENT ALGORITHMS
	# TAKES THE ACTION AND CHANGES AGENT ATTRIBUTES
	def takeAction(self, agent, action):
		nextState = self.nextState(agent, action)
		value = self.grid.grid[nextState[0],nextState[1]]
		if value != self.grid.edge_value and value != self.grid.done_reward and value > 0:
			self.grid.grid[nextState[0],nextState[1]] = 0
		if self.alg == "A2C" or self.alg == "PGM":
			self.grid.grid[nextState[0],nextState[1]] = 0
		agent.health += self.grid.normal_reward
		agent.health += value
		won = value == self.grid.done_reward
		lost = agent.health <= 0
		agent.done = won or lost
		agent.won = won
		agent.prev_state = agent.state
		agent.state = tuple(nextState)

		if value > 0:
			agent.fruits += 1

		agent.movements += 1

		if won:
			reward = 1
		elif lost: reward = -1
		else:
			reward = value
			if value == 0 and not self.alg=="PGM" and not self.alg=="A2C":
				reward = self.grid.normal_reward

		agent.totalreward += reward
		return reward

	def takeActionGA(self, agent, action):
		nextState = self.nextState(agent, action)
		value = self.grid.grid[nextState[0],nextState[1]]
		agent.health += self.grid.normal_reward
		agent.health += value
		won = value == self.grid.done_reward
		lost = agent.health < 0

		agent.done = won or lost
		agent.won = won
		agent.prev_state = agent.state
		agent.state = tuple(nextState)

		agent.movements += 1

		if won:
			reward = 1
		elif lost:
			reward = -1
		else:
			reward = value

		if agent.movements > (self.grid.padded_x+self.grid.padded_x):
			agent.done = True
			agent.won = False
			agent.health = -10
			reward = -2
		agent.totalreward += reward
		return reward

	# SHOW ENVIRONMENT IN CONSOLE
	def printBoard(self):
		grid = self.grid.grid.copy()
		for n in range(self.numAgents):
			state = self.agents[n].state
			grid[state[0],state[1]] += 1
		print(grid.round(1))

	# CHECK WHETHER ALL THE AGENTS HAVE FINISHED THEIR EPISODE
	def allFinished(self):
		done = True
		for n in range(self.numAgents):
			if not self.agents[n].done:
				done = False
		return done



	"""--------EVALUATION METHODS--------"""

	def evalStep(self, agent):
		env = self.grid.getEnvironment(agent.state).astype(np.float32)
		output = agent.forward(env)
		if self.alg=="PGM":
			act, log_action, value = self.reinforce.selectAction(output)
			action = self.actions[int(act)]
		else:
			action = self.actions[output.max(1)[1][0]]
		if self.alg == "GA":
			self.takeActionGA(agent, action)
		else:
			self.takeAction(agent, action)

	def loadEpochs(self, path):
		e = [os.path.join(path,m) for m in os.listdir(path)]
		e.sort(key=lambda x: int(x.split('/')[7].split('.')[0]))
		return e

	def evalEpisode(self,agent):
		self.csv_coords.write([agent.state[0], agent.state[1], agent.health])
		while not agent.done:
			self.evalStep(agent)
			self.newGeneralMovements += 1
			self.csv_coords.write([agent.state[0], agent.state[1], agent.health])


	def getStates(self, array, value):
		ts = np.where(array==value)
		v = []
		for i in range(len(ts[0])):
			v.append(ts[0][i])
			v.append(ts[1][i])
		return v

	def writeInfo(self,numAgents,epochs):
		self.csv_info.write([self.alg]) # algorithm
		self.csv_info.write([self.grid.padded_x, self.grid.padded_y]) # dimensions
		self.csv_info.write(self.getStates(self.grid.grid, self.grid.edge_value)) # padding states
		self.csv_info.write(self.getStates(self.grid.grid, self.grid.done_reward)) # final states
		self.csv_info.write(list(np.array(self.grid.walls).flatten())) # walls
		self.csv_info.write(self.grid.walls_values) # walls values
		self.csv_info.write([numAgents]) # number of agents
		self.csv_info.write([epochs]) # number of epochs
		self.csv_info.write([self.grid.visibleRad]) # Agent's visible radius and padding
		self.csv_info.write([self.grid.min_wall, self.grid.max_wall]) # Min and Max values of walls
		self.csv_info.close()

	def eval(self):
		agents = self.numAgents
		if self.alg=="GA":
			agents = int(self.numAgents*self.ga.pos)
		for n in range(agents):
			agent = self.agents[n]
			path = os.path.join(self.weights_path, self.alg, self.version, str(n))
			epochs = self.loadEpochs(path)
			for i,e in enumerate(epochs):
				self.csv_coords = CSV(self.alg, self.version, str(n), "coords", str(i))
				self.csv_info = CSV(self.alg, self.version, str(n), "info", str(i))

				model = torch.load(e)
				agent.loadWeights(model["state_dict"])
				self.reset()
				self.writeInfo(agents, len(epochs))
				self.evalEpisode(agent)
				self.csv_coords.close()
				self.csv_info.close()
				print("Evaluated agent {} in mutation {}. ".format(n,i), end='\r')
		print("\nEvaluation finished")

	def stats_eval(self):
		agents = self.numAgents
		if self.alg=="GA":
			agents = int(self.numAgents*self.ga.pos)
		for n in range(agents):
			agent = self.agents[n]
			path = os.path.join(self.weights_path, self.alg, self.version, str(n))
			epochs = self.loadEpochs(path)
			for i,e in enumerate(epochs):
				model = torch.load(e)
				agent.loadWeights(model["state_dict"])
				avgHealth=[]
				avgMvments=[]
				avgReward=[]
				winRate=[]
				for j in range(self.iterations):
					self.reset(random=True)
					while not agent.done:
						self.evalStep(agent)
						self.newGeneralMovements += 1
					avgHealth.append(agent.health)
					avgMvments.append(agent.movements)
					avgReward.append(agent.totalreward)
					winRate.append(1) if agent.won else winRate.append(0)
				l = len(avgHealth)
				print("Evaluated agent {} in epoch {}. ".format(n,i))
				print("\tAverage Health: {}\n\tAverage Movements: {}\n\tAverage Reward: {}\n\tWin Rate: {}\n\
						".format(sum(avgHealth)/l,sum(avgMvments)/l,sum(avgReward)/l,sum(winRate)/l))
