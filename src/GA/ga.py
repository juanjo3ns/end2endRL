import os
import numpy as np
import random
import torch
from IPython import embed
from collections import defaultdict


class GA:
	def __init__(self,
		agents,
		sigma=0.02):

		self.pos = 0.05 # Percentage Of Selection
		self.galpha = 0.5 # Decrement variance
		self.balpha = 0.0025 # Increment variance
		self.mutation = 0
		self.genes = {}
		self.elite = []
		self.agents = agents
		self.numAgents = len(self.agents.keys())
		self.sigma = sigma
		self.MIN_VARIANCE = 0.001
		self.MAX_VARIANCE = 0.08

	def _addNoise(self, network):
		with torch.no_grad():
			for param in network.parameters():
				noise = torch.randn(param.size()).cuda() * torch.tensor(self.sigma).cuda()
				param.add_(noise)
		return network

	def _getEliteNetworks(self):
		networks = []
		for e in self.elite:
			networks.append(self.agents[e].getNetwork())
		return networks

	def reset(self):
		self.elite.clear()
		self.genes = {}

	def selectElite(self):
		for n in range(self.numAgents):
			self.genes[n] = self.agents[n].totalreward
		for i in range(int(self.pos*self.numAgents)):
			selected = max(self.genes.keys(), key=(lambda key: self.genes[key]))
			self.elite.append(selected)
			del self.genes[selected]

	def generateNewAgents(self):
		self.mutation += 1
		networks = self._getEliteNetworks()
		for n in range(self.numAgents):
			enum = n%int(self.pos*self.numAgents)
			new_network = self._addNoise(networks[enum])
			self.agents[n].loadWeights(new_network.state_dict())

	def updateVariance(self, numElite):
		rate = numElite/self.numAgents
		if rate > self.pos and self.sigma > self.MIN_VARIANCE:
			self.sigma -= self.galpha*self.sigma*(1-rate)
		elif rate < self.pos and self.sigma < self.MAX_VARIANCE:
			self.sigma += self.balpha*self.sigma*(1-rate)
