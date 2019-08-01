import numpy as np
from IPython import embed
import torch

class ActorCritic:
	def __init__(self):
		self.gamma = 0.99
		self.action = 0
		self.log_action = 0
		self.entropy = 0
		self.value = 0

	def selectAction(self,output):
		dist, value = output
		action = dist.sample()
		self.value = value
		self.action = action
		self.log_action = dist.log_prob(action)
		self.entropy = dist.entropy().mean()
		return action

	def actorcritic(self, agent, reward, next_env):
		loss = 0
		reward = torch.Tensor([reward]).cuda()

		if agent.done:
			v_target = reward.detach()
		else:
			_, next_value = agent.forward(next_env)
			v_target = reward.detach() + self.gamma*next_value

		v_prediction = self.value
		advantage = v_prediction - v_target

		value_loss = advantage.pow(2)

		policy_loss = -self.log_action*advantage

		loss = policy_loss + 0.5*value_loss - 0.001*self.entropy

		agent.optim.zero_grad()
		loss.backward()
		agent.optim.step()

		agent.loss = loss.detach().cpu().item()
