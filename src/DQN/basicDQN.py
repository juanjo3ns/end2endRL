import os
import numpy as np
from tqdm import tqdm
from time import sleep
import random
from IPython import embed
from tensorboard_logger import configure, log_value, log_histogram
import torch
from src.General.Board import Board
from src.General.NN import QNet
from src.utils.sendTelegram import send

'''
MAIN CHANGES IN VERSION: 4.5.1
 - Very basic DQN implementation
 - Target update freq 50
 - init epsilon 0.5
 - lr 0.001

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

epsilon_scheduled = np.linspace(0.5,0.0001,2000)

board = Board(epsilon_scheduled,algorithm='basic-dqn')
'''
Load two Q functions approximators (neural networks)
 -> One of them will be used just to compute target Q values, and will be loaded
 	with Q weights every X episodes
 -> Second one will be used to estimate current Q values
'''
Q = QNet(board)
target_Q = QNet(board)
dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
atype = torch.cuda.LongTensor if torch.cuda.is_available() else torch.LongTensor
Q = Q.type(dtype)
target_Q = target_Q.type(dtype)

# Optimizer
optimizer = torch.optim.Adam(Q.parameters(), lr=0.001)
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


# ITERATION'S LOOP
for it in tqdm(range(board.numIterations)):

	initState = board.resetInitRandomly()

	# If we set up an experiment change, it will change the lava cells to check
	# if the algorithm is able to change its behaviour
	board.changeExperiment(it)
	# EPISODE'S LOOP
	done = False
	while not done:
		board_state = torch.from_numpy(board.getEnvironment(initState).astype(np.float32)).type(dtype)
		q_values = Q.predict(board_state.unsqueeze(0))
		max_q_value = q_values.max(1)[0]
		if random.random() > board.epsilon_scheduled[it]:
			action = board.actions[q_values.max(1)[1][0]]

		else:
			action = board.actions[np.random.choice(range(len(board.actions)))]

		reward, nextState, done = board.takeAction(initState, action)

		nextState_ = torch.from_numpy(board.getEnvironment(nextState).astype(np.float32)).type(dtype)
		next_q_value = target_Q.predict(nextState_.unsqueeze(0))
		max_next_q_value = next_q_value.detach().max(1)[0]

		if done:
			td_target = reward
			td_target = torch.from_numpy(np.array(reward).astype(np.float32)).type(dtype).unsqueeze(0)
		else:
			td_target = reward + board.gamma*max_next_q_value

		optimizer.zero_grad()
		loss = loss_fn(td_target, max_q_value)
		loss.backward()
		board.loss_list.append(loss.detach().cpu().numpy())

		for p in Q.parameters():
			p.grad.data.clamp_(-1, 1)
		optimizer.step()


		initState = nextState
		board.count[nextState]+=1
		if board.movements > board.maxSteps:
			break



	if it % board.target_update_freq == 0:
		target_Q.load_state_dict(Q.state_dict())
	if it %100==0:
		eval(Q)
		# send("Iteration number {}".format(it))
		torch.save(Q.state_dict(), 'model/{}/{}.pt'.format(board.version, it))
	if it % board.learning_freq == 0:
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
