from flask import Flask, jsonify, request, render_template, send_file
import threading
from helpers import *
import bridge as bdg
import json
from IPython import embed
from flask_cors import CORS
import shutil

app = Flask(__name__)

envs_path = '/data/envs'
data_path = '/data/src/templates/csvdata/'
weights_path = '/data/src/weights/'
tensor_path = '/data/src/tensorboard/'

cors = CORS(app)


@app.route('/envs', methods=['GET', 'POST', 'PUT'])
def add():
	if request.method == 'GET':
		if len(request.args)>0:
			version = request.args.get('version')
			return jsonify(getData(version))
		else:
			# response = flask.jsonify(getVersions())
			# response.headers.add('Access-Control-Allow-Origin', '*')
			return jsonify(getVersions())
			# return response
	elif request.method == 'POST' or request.method == 'PUT':
		data = request.get_json()
		saveData(data)
		return jsonify(getVersions())


@app.route('/train')
def train():
	version = request.args.get('version')
	data = getDataTraining(version)
	able, comment = checkingTrain(threading.active_count(), data)
	if able:
		thead = threading.Thread(target = bdg.train, args = (data,))
		thead.start()
	return jsonify(comment)


@app.route('/eval')
def eval():
	version = request.args.get('version')
	data = getDataTraining(version)
	able, comment = checkingEval(data)
	if able:
		bdg.eval(data)
		shutil.rmtree(os.path.join(weights_path, data['alg'], data['version']))
	return jsonify(comment)

@app.route('/del')
def delete():
	version = request.args.get('version')
	removeEnvironment(version)
	return jsonify("All files related to {} deleted!".format(version))

@app.route('/threed')
def threed():
	algorithm = request.args.get('algorithm')
	version = request.args.get('version')
	able, comment = checkingThreed(algorithm, version)
	if able:
		if os.path.exists(os.path.join(data_path, algorithm, 'current')):
			shutil.rmtree(os.path.join(data_path, algorithm, 'current'))
		shutil.copytree(os.path.join(data_path, algorithm, version), os.path.join(data_path, algorithm, 'current'))
	return jsonify(comment)

@app.route('/threeddqn')
def showdqn():
	return render_template('DQN/index.html', title='3D')

@app.route('/threedga')
def showga():
	return render_template('GA/index.html', title='3D')

@app.route('/threedpgm')
def showpgm():
	return render_template('RWB/index.html', title='3D')

@app.route('/threedac')
def showac():
	return render_template('A2C/index.html', title='3D')

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
	return send_file(subpath)


app.run(host='0.0.0.0', port=5000, debug=True)