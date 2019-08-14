from flask import Flask, jsonify, request
import threading
from helpers import *
import bridge as bdg
import json
from IPython import embed
from flask_cors import CORS
import shutil

app = Flask(__name__)

envs_path = '/data/envs'
data_path = '/data/demo/csvdata/'
weights_path = '/data/src/weights/'
tensor_path = '/data/src/tensorboard/'

cors = CORS(app)

@app.route('/')
def index():
	return 'Index Page'


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
	return 0

@app.route('/threed')
def threed():
	return 0

app.run(host='0.0.0.0', port=5000, debug=True)
