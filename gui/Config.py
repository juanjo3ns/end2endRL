import json
import os
import tkinter as tk
from tkinter import messagebox



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
        self.done_reward = "10"
        self.visibleRad = "1"
        self.min_wall = "-1"
        self.max_wall = "0"
        self.edge_value = "-1"
        self.normal_reward = "-0.04"
        self.numAgents = "1"
        self.height = 10
        self.width = 10

        self.epsmax = "0.6"
        self.epsmin = "0.0001"

        self.variance = "0.03"
        self.pos = "0.05"

        self.walls = list()
        self.finalstate = []
        self.initstate = []

        self.root = tk.Tk()


    def correctValues(self):
        if self.version == '':
            messagebox.showinfo('Introduce valid version', 'OK')
            return False
        if not self.alg == 'GA' and int(self.numAgents) > 1:
            print(self.numAgents, self.alg)
            messagebox.showinfo('MultiAgent not implemented in this algorithm', 'OK')
            return False
        if len(self.finalstate)==0 or len(self.initstate)==0:
            messagebox.showinfo('Configure valid final state and initial state', 'OK')
            return False
        if float(self.epsmax) > 1 or float(self.epsmax) < 0 or float(self.epsmin) > 1 or float(self.epsmin) < 0:
            messagebox.showinfo('Epsilon values in range [0,1]', 'OK')
            return False
        if float(self.pos) > 1 or float(self.pos) < 0:
            messagebox.showinfo('Percentage of selection in range [0,1]', 'OK')
            return False
        if int(self.health) < 0 or self.health == '':
            messagebox.showinfo('Health value has to be positive', 'OK')
            return False
        if int(self.iterations) < 0 or self.iterations == '':
            messagebox.showinfo('Iterations value has to be positive', 'OK')
            return False
        if int(self.batch_size) < 0 or self.batch_size == '':
            messagebox.showinfo('Batch size value has to be positive', 'OK')
            return False
        if int(self.savefreq) < 0 or self.savefreq == '':
            messagebox.showinfo('Save frequency value has to be positive', 'OK')
            return False
        return True

    def saveEnvironment(self):
        if self.correctValues():
            data = self.getJSONData()
            with open(os.path.join('./envs', self.version + '.json'), 'w') as f:
                json.dump(data, f)
            return True
        return False

    def loadEnvironment(self, version):
        with open(os.path.join('./envs', version + '.json'), 'r') as f:
            data = json.load(f)
        self.loadJSONData(data)

    def removeEnvironment(self):
        os.remove(os.path.join('./envs', self.version + '.json'))

    def getJSONData(self):
        data = {}
        data['version'] = self.version
        data['alg'] = self.alg
        data['tensorboard'] = self.tensorboard
        data['padding'] = self.padding
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
        data['finalstate'] = self.finalstate
        data['initstate'] = self.initstate
        data['height'] = self.height
        data['width'] = self.width
        return data


    def loadJSONData(self, data):
        self.version = data['version']
        self.alg = data['alg']
        self.tensorboard = data['tensorboard']
        self.padding = data['padding']
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
        self.finalstate = data['finalstate']
        self.initstate = data['initstate']
        self.height = data['height']
        self.width = data['width']
