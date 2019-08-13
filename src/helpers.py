import json
import os
from IPython import embed
import copy

envs_path = '/data/envs'

def getData(version):
    with open(os.path.join(envs_path, version), 'r') as f:
        data = json.load(f)
    return data

def getDataTraining(version):
    with open(os.path.join(envs_path, version), 'r') as f:
        raw_data = json.load(f)
    data = copy.deepcopy(raw_data)
    data['batch_size'] = data['batch_size']['value']
    data['variance'] = data['variance']['value']
    data['po'] = data['po']['value']
    data['numwalls'] = data['numwalls']['value']
    new_walls = []
    for walls in data['walls']:
        new_walls.append([int(walls.split('-')[0]),int(walls.split('-')[1])])
    data['walls'] = new_walls
    data['initstate'] = [int(data['initstate'][0].split('-')[0]), int(data['initstate'][0].split('-')[1])]
    data['finalstate'] = [int(data['finalstate'][0].split('-')[0]), int(data['finalstate'][0].split('-')[1])]
    data['height'] = data['height']
    data['width'] = data['width']

    print(data)
    return data

def saveData(data):
    with open(os.path.join(envs_path, data['version'] + '.json'), 'w') as f:
        json.dump(data, f)

def getVersions():
    return os.listdir(envs_path)
