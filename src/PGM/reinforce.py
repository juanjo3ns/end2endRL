import numpy as np
from IPython import embed
import torch

class Reinforce:
	def __init__(self):
		self.gamma = 0.9
		self.count = 0

	def selectAction(self,output):
		m, value = output
		action = m.sample()
		return action, m.log_prob(action), value

	def append(self, agent, value, action, reward):
		agent.baselines.append(value)
		agent.actions.append(action)
		agent.rewards.append(reward)

	def reinforce(self, agent):
		self.count+=1
		discounted_rewards = []
		R = 0
		for r in agent.rewards[::-1]:
			R = r + self.gamma * R
			discounted_rewards.insert(0, R)
		discounted_rewards = torch.Tensor(discounted_rewards).cuda()
		loss = 0
		for action, value, reward in zip(agent.actions, agent.baselines, discounted_rewards):
			reward_diff = reward - value
			loss += -action * reward
		# if self.count%20000==0:
			# embed()

		agent.optim.zero_grad()
		loss.backward()
		agent.optim.step()

		agent.loss = loss.detach().cpu().item()
		return discounted_rewards.sum(), 1 if agent.rewards[-1]==1 else 0
