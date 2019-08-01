import math
import argparse
import numpy as np
from tqdm import tqdm
from time import sleep
from IPython import embed
from src.General.Environment import Environment
from src.General.Seed import setSeed
from src.utils.utils import str2bool

parser = argparse.ArgumentParser()
parser.add_argument("--iterations", default=500, type=int,help="""Number of iterations/mutations""")
parser.add_argument("--seed", default=0, type=int,help="""Seed number""")
parser.add_argument("--version", default='0.0.0', type=str,help="""Version of experiment [x.x.x]""")
parser.add_argument("--sigma", default=0.04, type=float,help="""Noise Gaussian variance in GA""")
parser.add_argument("--env", default=6, type=int,help="""Environment number""")
parser.add_argument("--h", default=10, type=int,help="""Height of environment""")
parser.add_argument("--w", default=10, type=int,help="""Width of environment""")
parser.add_argument("--numAgents", default=1, type=int,help="""Environment number""")
parser.add_argument("--health", default=1, type=int,help="""Agent's health""")
parser.add_argument("--po", default=False, type=str2bool,help="""Environment is Partially Observable""")
parser.add_argument("--visibleRad", default=1, type=int,help="""Agent's visible radius but also padding in environment when not PO""")
parser.add_argument("--alg", default="DQN", type=str,help="""Use "PGM" or "GA" or "DQN" """)
parser.add_argument("--show", default=False, type=str2bool,help="""Print environment""")
parser.add_argument("--tbX", default=True, type=str2bool,help="""Tensorboard tbX""")
parser.add_argument("--save", default=False, type=str2bool,help="""Save weights""")
parser.add_argument("--onnx", default=False, type=str2bool,help="""Save weights for browser predictions""")
parser.add_argument("--save_freq", default=10, type=int,help="""Frequency weight's saving""")
parser.add_argument("--batch_size", default=1000, type=int,help="""Batch Size""")

args = parser.parse_args()
version = args.version
iterations = args.iterations
seed = args.seed
sigma = args.sigma
env = args.env
h = args.h
w = args.w
numAgents = args.numAgents
health = args.health
po = args.po
visibleRad = args.visibleRad
alg = args.alg
show = args.show
tbX = args.tbX
save = args.save
onnx = args.onnx
save_freq = args.save_freq
batch_size = args.batch_size

setSeed(seed)

eps_scheduled = lambda index: 0.0001 + (0.6 - 0.0001) * math.exp(-1. * index / int(iterations / 7))
eps=0.01


env = Environment(eps,
	eps_scheduled=eps_scheduled,
	iterations=iterations,
	sigma=sigma,
	env=env,
	height=h,
	width=w,
	numAgents=numAgents,
	health=health,
	po=po,
	visibleRad=visibleRad,
	alg=alg,
	tbX=tbX,
	save=save,
	onnx=onnx,
	save_freq=save_freq,
	batch_size=batch_size,
	version=version)

rewards_list = []
win_rate=0
for it in tqdm(range(iterations)):
	env.reset()
	# print(env.grid.grid.round(1))
	while not env.allFinished():
		env.step(it)
		env.newGeneralMovements += 1
		if show:
			env.printBoard()
			sleep(0.03)


	if alg=="DQN":
		env.env_dqn(it)

	elif alg=="GA":
		env.env_geneticalgorithms(it)

	elif alg=="PGM":
		rewards, won = env.env_reinforce()
		win_rate+=won
		rewards_list.append(rewards)
		# if it!=0:
		# 	print("Win rate: ", 100*win_rate/it, end="\r")
		if it%1000==0:
			ravg = sum(rewards_list)/len(rewards_list)
			print("Epoch {} ".format(it),ravg.item())

	env.logs(it)

if tbX:
	env.writer.close()
