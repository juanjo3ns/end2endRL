import matplotlib
matplotlib.use('Agg')
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from IPython import embed
import pandas as pd
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 75

def plot_value_function(V,contador, path):

	x_range = np.arange(0, len(V[0]))
	y_range = np.arange(0, len(V[0]))
	X, Y = np.meshgrid(x_range, y_range)
	Z = V

	fig = plt.figure(figsize=(20, 10))
	ax = fig.add_subplot(111, projection='3d')
	surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=matplotlib.cm.coolwarm, vmin=V.min(), vmax=V.max())
	ax.set_xlabel('Maze X')
	ax.set_ylabel('Maze Y')
	ax.set_zlabel('Values')
	ax.set_title(str(contador))
	ax.view_init(elev=25, azim=70)
	fig.colorbar(surf)
	plt.savefig(path)
	plt.close()

def values(V):

	x_range = np.arange(0, len(V[0]))
	y_range = np.arange(0, len(V[:,0]))
	X, Y = np.meshgrid(x_range, y_range)
	Z = V
	fig = plt.figure(figsize=(20, 10))
	ax = fig.add_subplot(111, projection='3d')
	surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=matplotlib.cm.coolwarm, vmin=V.min(), vmax=V.max())
	# Idk why but it's flipped X<->Y
	ax.set_xlabel('Maze Y')
	ax.set_ylabel('Maze X')
	ax.set_zlabel('Values')
	ax.view_init(elev=30, azim=10)
	fig.colorbar(surf)
	return fig

def arrows(x,y):

	t = np.arange(0, len(x[0]), 1)
	z = np.arange(0, len(x[:,0]), 1)
	X, Y = np.meshgrid(t,z)
	U=x
	V=y
	fig, ax = plt.subplots()
	q = ax.quiver(X, Y, U, V)
	ax.quiverkey(q, X=0.3, Y=1.1, U=10,
	         label='Agent directions', labelpos='E')
	return fig

def plot_heatmap(data, path, it):
	x_ax = np.array([v[0] for v in data.keys()])
	y_ax = np.array([v[1] for v in data.keys()])
	z_ax = np.array([data[v] for v in data.keys()])
	df = pd.DataFrame.from_dict(np.array([x_ax,y_ax,z_ax]).T)
	df.columns = ['X','Y','Z']
	pivotted= df.pivot('X','Y','Z')
	pivotted.fillna(0, inplace=True)
	pivotted = pivotted.astype(int)
	f, ax = plt.subplots(figsize=(12,10))
	ax.set_title(str(it))
	sns.heatmap(pivotted, annot=True, fmt="d", linewidths=.5, ax=ax)
	plt.savefig(path, dpi=75)
	plt.close()
