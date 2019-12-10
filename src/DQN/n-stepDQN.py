import os
import numpy as np
from tqdm import tqdm
from time import sleep
import random
from IPython import embed
from tensorboard_logger import configure, log_value, log_histogram
import torch
from src.General.Buffer import Buffer
from src.General.Board import Board
from src.General.NN import LightQNet
from src.utils.sendTelegram import send

'''
MAIN CHANGES IN VERSION: 4.3.3
 - Next state = state in n steps
 - steps 2
 - LightQNet

'''

manualSeed = 123123
np.random.seed(manualSeed)
random.seed(manualSeed)
torch.manual_seed(manualSeed)
torch.cuda.manual_seed(manualSeed)
torch.cuda.manual_seed_all(manualSeed)

torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True

# epsilon_scheduled = np.linspace(0.3,0.0001,2000)
import math
epsilon_scheduled = lambda index: 0.0001 + (0.3 - 0.0001) * math.exp(-1. * index / 500)

board = Board(epsilon_scheduled=epsilon_scheduled,algorithm='nstep-dqn', nstep=3)
buffer = Buffer(size=200000, batch_size=board.batch_size)
'''
Load two Q functions approximators (neural networks)
 -> One of them will be used just to compute target Q values, and will be loaded
 	with Q weights every X episodes
 -> Second one will be used to estimate current Q values
'''
Q = LightQNet(board)
target_Q = LightQNet(board)
dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
atype = torch.cuda.LongTensor if torch.cuda.is_available() else torch.LongTensor
Q = Q.type(dtype)
target_Q = target_Q.type(dtype)

# Optimizer
optimizer = torch.optim.Adam(Q.parameters(), lr=board.alpha_nn)
loss_fn = torch.nn.MSELoss()

path_out = "/data/src/tensorboard/DQN/" + board.version
configure(path_out, flush_secs=5)

#Folder to store weights, if it doesn't exists create it
if not os.path.exists('model/'):
	os.mkdir('model/')
if not os.path.exists(os.path.join('model', board.version)):
	os.mkdir(os.path.join('model', board.version))

def eval(q_fn):
	actions_legend = {0:"^",1:">",2:"v",3:"<"}
	baseline = []
	for state in board.states:
		board_state = torch.from_numpy(board.getEnvironment(state).astype(np.float32)).type(dtype)
		q_values = q_fn.predict(board_state.unsqueeze(0))
		action = q_values.max(1)[1][0].detach().cpu().numpy()
		baseline.append(actions_legend[int(action)])
	baseline = np.array(baseline).reshape(board.gridSize, board.gridSize)
	print(baseline)

def nstep(random,initState):
	trueInitState = initState
	treward = 0
	done = False
	for step in range(board.nstep):
		if random:
			action = board.actions[np.random.choice(range(len(board.actions)))]
		else:
			board_state = torch.from_numpy(board.getEnvironment(initState).astype(np.float32)).type(dtype)
			q_values = Q.predict(board_state.unsqueeze(0))
			action = board.actions[q_values.max(1)[1][0]]
		reward, nextState, done = board.takeAction(initState, action)

		if step == 0:
			trueInitAction = action
			trueNextState = nextState

		treward += reward*board.gamma**step
		initState = nextState
		if done:
			break

	return (trueInitState, board.actions.index(trueInitAction), nextState, treward, done, trueNextState)

def step(initState):

	if it > board.start_learning:
		if random.random() > board.epsilon_scheduled(it):
			with torch.no_grad():
				Q.eval()
				return nstep(False,initState)
		else:
			return nstep(True,initState)
	else:
		return nstep(True,initState)
	return nstep(True,initState)

# ITERATION'S LOOP
for it in tqdm(range(board.numIterations)):

	initState = board.resetInitRandomly()

	# If we set up an experiment change, it will change the lava cells to check
	# if the algorithm is able to change its behaviour
	board.changeExperiment(it)
	# EPISODE'S LOOP
	done = False
	while not done:

		# When we train, we need the last state of the n-step in order
		# to compute the max q values of that final state, so we store the last state
		# but we just move to the very next state.
		initState, action, nextState, reward, done, trueNextState = step(initState)
		buffer.store((initState, action, nextState, reward, 0 if done else 1))

		initState = nextState
		board.count[nextState]+=1
		if board.movements > board.maxSteps:
			break

	if it > board.start_learning and it % board.learning_freq == 0:
		for x in range(300):
			Q.train()
			sample_data = buffer.sample()
			state_batch = torch.from_numpy(np.array([board.getEnvironment(x).astype(np.float32) for x in sample_data['state']])).type(dtype)
			action_batch = torch.from_numpy(np.array(sample_data['action'])).type(atype)
			next_state_batch = torch.from_numpy(np.array([board.getEnvironment(x).astype(np.float32) for x in sample_data['next_state']])).type(dtype)
			reward_batch = torch.from_numpy(np.array(sample_data['reward'])).type(dtype)
			done_batch = torch.from_numpy(np.array(sample_data['done'])).type(dtype)

			all_q_values = Q.predict(state_batch)
			# We pick the q value that each action indicates, to do that we choose
			# from dimension 1 with the 'transposed' actions
			q_values = all_q_values.gather(1,action_batch.unsqueeze(1))
			next_q_values = target_Q.predict(next_state_batch)
			# We pick the maximum values in dimension 1, for each row, and then
			# [0] is because it returns the index as well
			max_next_q_values = next_q_values.detach().max(1)[0]
			# multiply target by done, because if we are done, there are not other next q values
			td_target = reward_batch + board.gamma*max_next_q_values*done_batch
			td_target = td_target.unsqueeze(1)
			optimizer.zero_grad()
			loss = loss_fn(td_target, q_values)
			loss.backward()
			board.loss_list.append(loss.detach().cpu().numpy())

			for p in Q.parameters():
				p.grad.data.clamp_(-1, 1)

			optimizer.step()




	if it % board.target_update_freq == 0 and it > board.start_learning:
		target_Q.load_state_dict(Q.state_dict())
	if it %100==0:
		eval(Q)
		# send("Iteration number {}".format(it))
		torch.save(Q.state_dict(), 'model/{}/{}.pt'.format(board.version, it))
	if it > board.start_learning and it % board.learning_freq == 0:
		if len(board.loss_list)==0:
			avg_loss = last_loss
		else:
			avg_loss = sum(board.loss_list)/len(board.loss_list)
		last_loss = avg_loss
		board.loss_list.clear()
		log_value("Loss", avg_loss, it)
	log_value("Total_reward", board.totalreward, it)
	log_value("Movements", board.movements, it)
	if it % board.plotStep==0:
		board.plotValues(it, board.Q)
		board.plotHeatmap(it)

board.generateGIF(board.heatmap_path)