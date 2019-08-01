import numpy as np
import argparse
from IPython import embed
from src.General.Environment import Environment
from src.General.Seed import setSeed
from src.utils.utils import str2bool

parser = argparse.ArgumentParser()
parser.add_argument("--version", default='0.0.0', type=str,help="""Version of experiment [x.x.x]""")
parser.add_argument("--seed", default=0, type=int,help="""Seed number""")
parser.add_argument("--stats", default=False, type=str2bool,help="""Infer stats without saving csv files""")
parser.add_argument("--iterations", default=100, type=int,help="""Number of iterations/mutations""")
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

args = parser.parse_args()
env = args.env
stats = args.stats
iterations = args.iterations
seed = args.seed
h = args.h
w = args.w
version = args.version
sigma = args.sigma
numAgents = args.numAgents
health = args.health
po = args.po
visibleRad = args.visibleRad
alg = args.alg
show = args.show

setSeed(seed)


env = Environment(
	env=env,
	iterations=iterations,
	height=h,
	width=w,
    po=po,
    visibleRad=visibleRad,
	sigma=sigma,
	numAgents=numAgents,
	health=health,
	alg=alg,
	version=version)

if stats:
	env.stats_eval()
else:
	env.eval()
