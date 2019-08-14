import sys
import os
import numpy as np
import random
from time import time
from tqdm import tqdm
from IPython import embed
from tensorboard_logger import configure, log_value, log_histogram
import torch
from src.General.Buffer import Buffer
from src.General.Board import Board
from src.General.NN import VNet, PolicyNet

'''
MAIN CHANGES IN VERSION: 0.0.0
'''
version = sys.argv[1]

manualSeed = 123123
np.random.seed(manualSeed)
random.seed(manualSeed)
torch.manual_seed(manualSeed)
torch.cuda.manual_seed(manualSeed)
torch.cuda.manual_seed_all(manualSeed)

torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True


board = Board(algorithm='a2c',version=version, exp=4)

Policy = PolicyNet(board)
V = VNet(board)
dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
atype = torch.cuda.LongTensor if torch.cuda.is_available() else torch.LongTensor
Policy = Policy.type(dtype)
V = V.type(dtype)
Policy.apply(Policy.init_weights)
V.apply(V.init_weights)

# Optimizer
optimPolicy = torch.optim.Adam(Policy.parameters(), lr=board.alpha_actor)
optimV = torch.optim.Adam(V.parameters(), lr=board.alpha_critic)
loss_fn = torch.nn.MSELoss()

path_out = "/data/src/tensorboard/RWB/" + board.version
configure(path_out, flush_secs=5)

# Folder to store weights, if it doesn't exists create it
if not os.path.exists(os.path.join('model')):
	os.mkdir(os.path.join('model'))
if not os.path.exists(os.path.join('model', board.version)):
	os.mkdir(os.path.join('model', board.version))

for it in tqdm(range(board.numIterations)):

	initState = board.resetInitRandomly()
	done = False
	values_loss = []
	policies_loss = []
	while not done:
		with torch.no_grad():
			board_state = torch.from_numpy(board.getEnvironment(initState).astype(np.float32)).type(dtype)
			actions_probs = Policy.forward(board_state)
			m = torch.distributions.Multinomial(probs=actions_probs[0])
			action = m.sample()
			act = board.actions[action.max(0)[1]]
			log_action = m.log_prob(action)

			reward, nextState, done = board.takeAction(initState, act)

			initState = nextState

		board_next_state = torch.from_numpy(board.getEnvironment(nextState).astype(np.float32)).type(dtype)
		v_target = reward + board.gamma*V.forward(board_next_state)[0][0]

		v_prediction = V.forward(board_state)[0][0]
		advantage = v_prediction - v_target.detach()

		value_loss = advantage.pow(2)
		values_loss.append(value_loss.detach().cpu().numpy())

		log_action.requires_grad = True
		policy_loss = -log_action*advantage.detach()
		policies_loss.append(policy_loss.detach().cpu().numpy())

		optimV.zero_grad()
		value_loss.backward()
		optimV.step()

		optimPolicy.zero_grad()
		policy_loss.backward()
		optimPolicy.step()

	if len(values_loss)>0:
		log_value("Loss", sum(values_loss)/len(values_loss), it)
		log_value("Policy loss", sum(policies_loss)/len(policies_loss), it)
	log_value("Total_reward", board.totalreward, it)
	log_value("Movements", board.movements, it)
