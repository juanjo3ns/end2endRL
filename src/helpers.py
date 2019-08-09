import json
import os

envs_path = '/data/envs'

def getData(version):
    with open(os.path.join(envs_path, version + '.json'), 'r') as f:
        data = json.load(f)
    return data

def saveData(data):
    with open(os.path.join(envs_path, data['version'] + '.json'), 'w') as f:
        json.dump(data, f)
