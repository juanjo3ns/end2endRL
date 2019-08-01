import torch
import torch.nn as nn
import torch.nn.functional as F
from IPython import embed


class QNet(nn.Module):
	def __init__(self, channels, height, width):
		super(QNet, self).__init__()

		self.fc1 = nn.Linear(channels * height * width,
							 5 * height * width)
		self.fc2 = nn.Linear(5 * height * width,
							 6 * height * width)
		self.fc3 = nn.Linear(6 * height * width,
							 3 * height * width)
		self.fc4 = nn.Linear(3 * height * width, 4)

	def forward(self, x):
		(_, C, H, W) = x.data.size()
		x = x.view(-1, C * H * W)
		x = F.relu(self.fc1(x))
		x = F.relu(self.fc2(x))
		x = F.relu(self.fc3(x))
		return self.fc4(x)

class LightQNet(nn.Module):
	def __init__(self, channels, height, width):
		super(LightQNet, self).__init__()

		self.fc1 = nn.Linear(channels * height * width,
							 2 * height * width)
		self.fc2 = nn.Linear(2 * height * width, 4)

	def forward(self, x):
		(_, C, H, W) = x.data.size()
		x = x.view(-1, C * H * W)
		x = F.relu(self.fc1(x))
		return self.fc2(x)

class PolicyNet(nn.Module):
	def __init__(self, h, w):
		super(PolicyNet, self).__init__()
		self.DROP_MAX = 0.3
		self.DROP_MIN = 0.05
		self.DROP_OVER = 200000
		self.dropout = lambda iter: (self.DROP_MAX - self.DROP_MIN) * max(0, (1 - iter / self.DROP_OVER)) + self.DROP_MIN
		self.fc1 = nn.Linear(h * w + 3, 2 * h * w)
		self.fc2 = nn.Linear(2 * h * w, 4+1)

	def forward(self, x, it):
		x = F.tanh(x)
		x = F.relu(self.fc1(x))
		# embed()
		x = self.fc2(x)
		drop = self.dropout(it)
		d = nn.Dropout(drop, True)
		scores = d(x[:4])
		scores = F.softmax(scores, dim=0)
		value = x[4]
		m = torch.distributions.Categorical(scores)
		return m, value

	def init_weights(self, m):
		if type(m) == nn.Linear:
			nn.init.xavier_uniform_(m.weight)
			m.bias.data.fill_(0.01)

class ActorCritic(nn.Module):
	def __init__(self,c, h, w):
		super(ActorCritic, self).__init__()

		self.actor = nn.Sequential(
			nn.Linear(h*w + 3, 256),
			nn.ReLU(),
			nn.Linear(256, 4),
			nn.Softmax(dim=0)
		)
		self.critic = nn.Sequential(
			nn.Linear(h*w + 3, 256),
			nn.ReLU(),
			nn.Linear(256,512),
			nn.ReLU(),
			nn.Linear(512,256),
			nn.ReLU(),
			nn.Linear(256,1)
		)

	def forward(self, x, it):
		probs = self.actor(x)
		value = self.critic(x)
		dist = torch.distributions.Categorical(probs)
		return dist, value
