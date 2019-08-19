import json
import os
from IPython import embed
import copy
import shutil


envs_path = '/data/envs'
data_path = '/data/src/templates/csvdata/'
weights_path = '/data/src/weights/'
tensor_path = '/data/src/tensorboard/'

def getData(version):
	with open(os.path.join(envs_path, version), 'r') as f:
		data = json.load(f)
	return data

def getDataTraining(version):
	with open(os.path.join(envs_path, version), 'r') as f:
		raw_data = json.load(f)
	data = copy.deepcopy(raw_data)
	data['batch_size'] = int(data['batch_size']['value'])
	data['variance'] = float(data['variance']['value'])
	data['po'] = data['po']['value']
	data['numwalls'] = int(data['numwalls']['value'])
	data['iterations'] = int(data['iterations'])
	data['savefreq'] = int(data['savefreq'])
	data['visibleRad'] = int(data['visibleRad'])
	data['normal_reward'] = float(data['normal_reward'])
	data['min_wall'] = float(data['min_wall'])
	data['max_wall'] = float(data['max_wall'])
	data['seed'] = int(data['seed'])
	data['done_reward'] = int(data['done_reward'])
	data['edge_value'] = int(data['edge_value'])
	data['numAgents'] = int(data['numAgents'])
	data['epsmax'] = float(data['epsmax'])
	data['epsmin'] = float(data['epsmin'])
	data['pos'] = float(data['pos']['value'])
	data['health'] = int(data['health'])

	new_walls = []
	if data['alg']=="DQN" or data['alg'] =="GA":
		for walls in data['walls']:
			new_walls.append([int(walls.split('-')[0]),int(walls.split('-')[1])])
		data['walls'] = new_walls
		data['initstate'] = [int(data['initstate'][0].split('-')[0]), int(data['initstate'][0].split('-')[1])]
		data['finalstate'] = [int(data['finalstate'][0].split('-')[0]), int(data['finalstate'][0].split('-')[1])]
		data['walls_values'] = [float(w) for w in data['walls_values']]
	data['height'] = data['height']
	data['width'] = data['width']
	return data

def saveData(data):
	with open(os.path.join(envs_path, data['version'] + '.json'), 'w') as f:
		json.dump(data, f)

def getVersions():
	return os.listdir(envs_path)

def checkingTrain(config, data):
	if data['saveweights'] and os.path.exists(os.path.join(weights_path, data['alg'], data['version'])):
		return False, "Weights already exist for this experiment."
	elif data['tensorboard'] and os.path.exists(os.path.join(tensor_path, data['alg'], data['version'])):
		return False, "Tensorboard logs already exist for this experiment."
	elif not config.thread is None:
		return False, "Someone is already training..."
	return True, "Training started!"

def checkingEval(data):
	if os.path.exists(os.path.join(data_path, data['alg'], data['version'])):
		return False, "CSV files already exist for this experiment."
	elif not os.path.exists(os.path.join(weights_path, data['alg'], data['version'])):
		return False, "There are no weights for this version! Make sure to save environment with save weights CheckBox and then train it."
	return True, "Evaluation finished!"

def checkingThreed(algorithm, version):
	if not os.path.exists(os.path.join(data_path, algorithm, version)):
		return False, "There are no CSV files stored. Make sure to evaluate the environment."
	return True, "Openning new tab..."

def removeEnvironment(version):
	algorithm = version.split('.')[0]
	os.remove(os.path.join('../envs', version + '.json'))
	for path in [weights_path, tensor_path, data_path]:
		if os.path.exists(os.path.join(path, algorithm, version)):
			shutil.rmtree(os.path.join(path, algorithm, version))
