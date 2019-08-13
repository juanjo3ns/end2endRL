import os
import numpy as np
import random
import torch
from IPython import embed
from collections import defaultdict
from random import choice
from src.General.Buffer import Buffer
from src.General.NN import QNet, LightQNet, PolicyNet, ActorCritic

class Agent:
	def __init__(self,
				height=10,
				width=3,
				channels = 3,
				health=1,
				alg="DQN",
				visibleRad=1,
				po=False,
				target_freq=48,
				batch_size=1000,
				nstep=1):

		# AGENT PARAMETERS
		self.initial_health = health
		self.health = health
		self.movements = 0
		self.state = None
		self.prev_state = None
		self.done = False
		self.won = False
		self.totalreward = 0
		self.counter = 0
		self.fruits = 0

		# CUSTOM PARAMETERS
		self.visibleRad = visibleRad
		self.po = po
		self.alg = alg # Indicates wether DQN, GA or PGM
		self.channels = channels
		# Environment shape, useful for neural network
		self.height = height
		self.width = width

		# NN parameters
		self.gamma = 0.90
		self.alpha = 0.1
		self.alpha_nn = 1e-4
		self.weight_decay = 1e-5
		self.start_learning = 50
		self.learning_freq = 1
		self.target_update_freq = target_freq
		self.batch_size = batch_size
		self.loss = 0

		# BUFFER INITIALIZATION FOR DQN VARIANTS
		self.buffer = Buffer(size=20000, batch_size=self.batch_size)

		# LISTS INITIALIZATION FOR PGM
		self.baselines = list()
		self.rewards = list()
		self.actions = list()

		# NN INITIALIZATION
		self.nn = None
		self.target_nn = None
		self.dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
		self.atype = torch.cuda.LongTensor if torch.cuda.is_available() else torch.LongTensor
		self.optim = None
		self.loss_fn = None
		self.initNN()

		# Path out for model's weights
		self.path_out = '/data/src/weights'

	def initNN(self):
		if self.po:
			h = w = 1 + self.visibleRad*2
		else:
		# [IF WE FINALLY ADD PADDING TO ALL ENVIRONMENTS I SHOULD ADD 2VRAD+1 TO H AND W]
			h = self.height + self.visibleRad*2
			w = self.width + self.visibleRad*2
			# h = self.height
			# w = self.width
		if self.alg=="DQN":
			self.nn = QNet(self.channels, h, w)
			self.target_nn = QNet(self.channels, h, w)
			self.target_nn.type(self.dtype)
			self.target_nn.apply(self.init_weights)
			self.optim = torch.optim.Adam(self.nn.parameters(), lr=self.alpha_nn)
			self.loss_fn = torch.nn.MSELoss()
		if self.alg=="GA":
			self.nn = QNet(self.channels, h, w)
		if self.alg=="RWB":
			self.nn = PolicyNet(h, w)
			self.optim = torch.optim.Adam(self.nn.parameters(), lr=self.alpha_nn, weight_decay=self.weight_decay)
			self.loss_fn = torch.nn.MSELoss()
		if self.alg=="A2C":
			self.nn = ActorCritic(self.channels, h, w)
			self.optim = torch.optim.Adam(self.nn.parameters(), lr=self.alpha_nn, weight_decay=self.weight_decay)
			self.loss_fn = torch.nn.MSELoss()
		self.nn.type(self.dtype)
		# self.nn.apply(self.init_weights)

	def init_weights(self, m):
		if type(m) == torch.nn.Linear:
			torch.nn.init.xavier_uniform_(m.weight)
			m.bias.data.fill_(0.01)

	def reset(self, initState):
		self.health = self.initial_health
		self.movements = 0
		self.totalreward = 0
		self.state = (initState[0],initState[1])
		self.prev_state = self.state
		self.done = False
		self.won = False
		self.loss = 0
		self.baselines.clear()
		self.rewards.clear()
		self.actions.clear()
		self.counter += 1
		self.fruits = 0

	def forward(self, env, it=0):
		if self.alg=="RWB" or self.alg=="A2C":
			x = (self.state[0] - self.visibleRad) / self.height
			y = (self.state[1] - self.visibleRad) / self.width
			env = env.flatten()
			env = np.concatenate((env, [self.health, x, y]))
			env_state = torch.from_numpy(env).type(self.dtype)
			return self.nn.forward(env_state, it)
		else:
			with torch.no_grad():
				env_state = torch.from_numpy(env).type(self.dtype).unsqueeze(0)
				return self.nn.forward(env_state)

	# In GA we need to load the best weights into every agent
	def loadWeights(self, weights):
		self.nn.load_state_dict(weights)

	# In DDQN every N epochs you have to copy the weights to the targetNN
	def updateTargetNN(self):
		self.target_nn.load_state_dict(self.nn.state_dict())

	# Get main NN
	def getNetwork(self):
		return self.nn

	# Save model and weights
	def saveModel(self, version, n, epoch):
		base_path = os.path.join(self.path_out, self.alg)
		version_path = os.path.join(base_path, version)
		agent_path = os.path.join(version_path, str(n))

		epoch_path = os.path.join(agent_path, '{}.pt'.format(epoch))
		if not os.path.isdir(self.path_out):
			os.mkdir(self.path_out)
		if not os.path.isdir(base_path):
			os.mkdir(base_path)
		if not os.path.isdir(version_path):
			os.mkdir(version_path)
		if not os.path.isdir(agent_path):
			os.mkdir(agent_path)

		torch.save({
			'agent': n,
			'state_dict': self.nn.state_dict(),
			'optimizer': self.optim},
			epoch_path)
