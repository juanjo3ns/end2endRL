import json
import os



class Config():
    def __init__(self):

        self.version = 'DQN.0.0'
        self.alg = 'DQN'
        self.tensorboard = False
        self.padding = False
        self.saveweights = False
        self.po = False

        self.iterations = "10000"
        self.savefreq = "1000"
        self.batch_size = "1000"
        self.health = "20"
        self.numwalls = "15"
        self.done_reward = "10"
        self.visibleRad = "1"
        self.min_wall = "-1"
        self.max_wall = "0"
        self.edge_value = "-1"
        self.normal_reward = "-0.04"
        self.numAgents = "1"
        self.height = 10
        self.width = 10
        self.seed = "0"

        self.epsmax = "0.6"
        self.epsmin = "0.0001"

        self.variance = "0.03"
        self.pos = "0.05"

        self.walls = list()
        self.walls_values = []
        self.finalstate = []
        self.initstate = []


    def correctValues(self):
        if self.version == '':
            return False
        if not self.alg == 'GA' and int(self.numAgents) > 1:
            return False
        if len(self.finalstate)==0 or len(self.initstate)==0:
            return False
        if float(self.epsmax) > 1 or float(self.epsmax) < 0 or float(self.epsmin) > 1 or float(self.epsmin) < 0:
            return False
        if float(self.pos) > 1 or float(self.pos) < 0:
            return False
        if int(self.health) < 0 or self.health == '':
            return False
        if int(self.iterations) < 0 or self.iterations == '':
            return False
        if int(self.batch_size) < 0 or self.batch_size == '':
            return False
        if int(self.savefreq) < 0 or self.savefreq == '':
            return False
        return True

    def saveEnvironment(self):
        if self.correctValues():
            data = self.getJSONData()
            with open(os.path.join('../envs', self.version + '.json'), 'w') as f:
                json.dump(data, f)
            return True
        return False

    def loadEnvironment(self, version):
        with open(os.path.join('../envs', version + '.json'), 'r') as f:
            data = json.load(f)
        self.loadJSONData(data)

    def removeEnvironment(self):
        os.remove(os.path.join('../envs', self.version + '.json'))

    def getJSONData(self):
        data = {}
        data['version'] = self.version
        data['alg'] = self.alg
        data['tensorboard'] = self.tensorboard
        data['saveweights'] = self.saveweights
        data['po'] = self.po
        data['iterations'] = int(self.iterations)
        data['savefreq'] = int(self.savefreq)
        data['batch_size'] = int(self.batch_size)
        data['health'] = int(self.health)
        data['done_reward'] = float(self.done_reward)
        data['visibleRad'] = int(self.visibleRad)
        data['min_wall'] = float(self.min_wall)
        data['max_wall'] = float(self.max_wall)
        data['edge_value'] = int(self.edge_value)
        data['normal_reward'] = float(self.normal_reward)
        data['numAgents'] = int(self.numAgents)
        data['epsmax'] = float(self.epsmax)
        data['epsmin'] = float(self.epsmin)
        data['variance'] = float(self.variance)
        data['pos'] = float(self.pos)
        data['walls'] = self.walls
        data['numwalls'] = self.numwalls
        data['walls_values'] = self.walls_values
        data['finalstate'] = self.finalstate
        data['initstate'] = self.initstate
        data['height'] = self.height
        data['width'] = self.width
        data['seed'] = int(self.seed)
        return data


    def loadJSONData(self, data):
        self.version = data['version']
        self.alg = data['alg']
        self.tensorboard = data['tensorboard']
        self.saveweights = data['saveweights']
        self.po = data['po']
        self.iterations = str(data['iterations'])
        self.savefreq = str(data['savefreq'])
        self.batch_size = str(data['batch_size'])
        self.health = str(data['health'])
        self.done_reward = str(data['done_reward'])
        self.visibleRad = str(data['visibleRad'])
        self.min_wall = str(data['min_wall'])
        self.max_wall = str(data['max_wall'])
        self.edge_value = str(data['edge_value'])
        self.normal_reward = str(data['normal_reward'])
        self.numAgents = str(data['numAgents'])
        self.epsmax = str(data['epsmax'])
        self.epsmin = str(data['epsmin'])
        self.variance = str(data['variance'])
        self.pos = str(data['pos'])
        self.walls = data['walls']
        self.walls_values = data['walls_values']
        self.numwalls = data['numwalls']
        self.finalstate = data['finalstate']
        self.initstate = data['initstate']
        self.height = data['height']
        self.width = data['width']
        self.seed = str(data['seed'])
