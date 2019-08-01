import os
import numpy as np
import sys
import random
from tqdm import tqdm
from IPython import embed
from tensorboard_logger import configure, log_value, log_histogram
import torch
from src.General.Buffer import Buffer
from src.General.Board import Board
from src.General.NN import VNet, PolicyNet
# from src.utils.sendTelegram import send

'''
MAIN CHANGES IN VERSION: 0.0.0
'''

seed = int(sys.argv[1])
version = sys.argv[2]

manualSeed = seed
np.random.seed(manualSeed)
random.seed(manualSeed)
torch.manual_seed(manualSeed)
torch.cuda.manual_seed(manualSeed)
torch.cuda.manual_seed_all(manualSeed)

torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True


board = Board(algorithm='reinforce',version=version, exp=4)

Policy = PolicyNet(board)
dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
atype = torch.cuda.LongTensor if torch.cuda.is_available() else torch.LongTensor
Policy = Policy.type(dtype)
Policy.apply(Policy.init_weights)

# Optimizer
optimPolicy = torch.optim.Adam(Policy.parameters(), lr=board.alpha_nn)
loss_fn = torch.nn.MSELoss()
eps = np.finfo(np.float32).eps.item()

path_out = "/data/src/tensorboard/PGM/" + board.version
configure(path_out, flush_secs=5)

# Folder to store weights, if it doesn't exists create it
if not os.path.exists(os.path.join('model')):
	os.mkdir(os.path.join('model'))
if not os.path.exists(os.path.join('model', board.version)):
	os.mkdir(os.path.join('model', board.version))

def discounted_reward(rewards, gamma):
	final_rewards = np.zeros(len(rewards))
	G = 0
	for i, r in enumerate(rewards[::-1]):
		final_rewards[len(rewards)-1-i] = r + G*gamma
		G = final_rewards[len(rewards)-1-i]
	return final_rewards

def generateEpisode(board, it):
	e_values = []
	e_actions = []
	e_rewards = []

	initState = board.resetInitRandomly()
	done = False
	while not done:
		with torch.no_grad():
			board_state = torch.from_numpy(board.getEnvironment(initState).astype(np.float32)).type(dtype)
			actions_probs, value = Policy.forward(board_state.unsqueeze(0))

			m = torch.distributions.Multinomial(probs=actions_probs[0])
			action = m.sample()
			act = board.actions[action.max(0)[1]]
			log_action = m.log_prob(action)

			reward, nextState, done = board.takeAction(initState, act)

			e_values.append(value)
			e_actions.append(log_action)
			e_rewards.append(reward)

			initState = nextState

	return e_values, e_actions, e_rewards

for it in tqdm(range(board.numIterations)):
	values, actions, rewards = generateEpisode(board, it)
	discounted_rewards = discounted_reward(rewards, board.gamma)

	# Normalize rewards if needed
	if len(rewards)!=1:
		discounted_rewards = (discounted_rewards-discounted_rewards.mean())/(discounted_rewards.std() + eps)
	baseline_target = torch.from_numpy(discounted_rewards.astype(np.float32)).type(dtype)
	# baseline_target.requires_grad = True
	baseline_target = baseline_target.unsqueeze(1)
	actions = torch.stack(actions,dim=0).unsqueeze(1)
	actions.requires_grad = True
	values = torch.stack(values)
	values.requires_grad = True
	policy_loss = -actions*(baseline_target-values)
	policy_loss = policy_loss.mean()
	loss_values = torch.nn.functional.smooth_l1_loss(values, baseline_target)
	loss = policy_loss + loss_values

	optimPolicy.zero_grad()
	loss.backward()
	optimPolicy.step()

	log_value("Policy loss", loss, it)
	log_value("Total_reward", board.totalreward, it)
	log_value("Movements", board.movements, it)
