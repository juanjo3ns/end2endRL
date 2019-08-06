import csv
import os

class CSV:
	def __init__(self,algorithm, env, agent, type, file):
		self.path = '/data/demo/csvdata'
		if not os.path.exists(self.path):
			os.mkdir(self.path)
		if not os.path.exists(os.path.join(self.path, algorithm)):
			os.mkdir(os.path.join(self.path, algorithm))
		if not os.path.exists(os.path.join(self.path, algorithm, env)):
			os.mkdir(os.path.join(self.path, algorithm, env))
		if not os.path.exists(os.path.join(self.path, algorithm, env, agent)):
			os.mkdir(os.path.join(self.path, algorithm, env, agent))
		if not os.path.exists(os.path.join(self.path, algorithm, env, agent, type)):
			os.mkdir(os.path.join(self.path, algorithm, env, agent, type))

		self.file = file
		self.csvfile = open(os.path.join(self.path, algorithm, env, agent, type, self.file + '.csv'), 'w')
		self.csvwriter = csv.writer(self.csvfile, delimiter=',')

	def write(self, row):
		self.csvwriter.writerow(row)
	def close(self):
		self.csvfile.close()
