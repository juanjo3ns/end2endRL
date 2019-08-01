import numpy as np
from IPython import embed
import torch

class DDQN:
	def __init__(self):
		self.gamma = 0.99

	def train(self, agent, states, next_states, actions, rewards, dones):
		agent.nn.train()
		state_batch = torch.from_numpy(states).type(agent.dtype)
		action_batch = torch.from_numpy(actions).type(agent.atype)
		next_state_batch = torch.from_numpy(next_states).type(agent.dtype)
		reward_batch = torch.from_numpy(rewards).type(agent.dtype)
		done_batch = torch.from_numpy(dones).type(agent.dtype)

		all_q_values = agent.nn.forward(state_batch)
		# We pick the q value that each action indicates, to do that we choose
		# from dimension 1 with the 'transposed' actions
		q_values = all_q_values.gather(1,action_batch.unsqueeze(1))

		''' DOUBLE DQN MAGIC '''
		# Select actions with Q network and get q values from target Q network
		select_action = agent.nn.forward(next_state_batch)
		target_q_values = agent.target_nn.forward(next_state_batch)
		next_q_values = target_q_values.gather(1,select_action.max(1)[1].unsqueeze(1))

		# multiply target by done, because if we are done, there are not other next q values
		td_target = reward_batch.unsqueeze(1) + self.gamma*next_q_values*done_batch.unsqueeze(1)
		agent.optim.zero_grad()
		loss = agent.loss_fn(td_target, q_values)
		loss.backward()
		agent.loss = loss.detach().cpu().numpy()

		for p in agent.nn.parameters():
			p.grad.data.clamp_(-1, 1)

		agent.optim.step()
