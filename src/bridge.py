import math
import numpy as np
from tqdm import tqdm
from time import sleep
from IPython import embed
from src.General.Environment import Environment
from src.General.Seed import setSeed
from src.General.Grid import Grid

DQN = "DQN"
GA = "GA"
PGM = "PGM"

def initializeEnv(data):
    grid = Grid(data)
    eps_scheduled = lambda index: data['epsmin'] + (data['epsmax'] - data['epsmin']) * math.exp(-1. * index / int(data['iterations'] / 7))
    env = Environment(
        grid,
        eps_scheduled=eps_scheduled,
    	iterations=data['iterations'],
    	sigma=data['variance'],
        pos=data['pos'],
    	height=data['height'],
    	width=data['width'],
    	numAgents=data['numAgents'],
    	health=data['health'],
    	po=data['po'],
    	visibleRad=data['visibleRad'],
    	alg=data['alg'],
    	tbX=data['tensorboard'],
    	save=data['saveweights'],
    	save_freq=data['savefreq'],
    	batch_size=data['batch_size'],
    	version=data['version'])
    return env


def train(data):
    setSeed(data['seed'])
    env = initializeEnv(data)
    for it in tqdm(range(data['iterations'])):
    	env.reset()
    	while not env.allFinished():
    		env.step(it)
    		env.newGeneralMovements += 1

    	if data['alg']==DQN:
    		env.env_dqn(it)

    	elif data['alg']==GA:
    		env.env_geneticalgorithms(it)

    	elif data['alg']==PGM:
    		rewards, won = env.env_reinforce()

    	env.logs(it)

    if env.tbX:
    	env.writer.close()

def eval(data):
    setSeed(data['seed'])
    data['health'] = 1
    env = initializeEnv(data)
    env.eval()
