from flask import Flask, jsonify, request
from helpers import getData, saveData, getVersions, getDataTraining
import bridge as bdg
import json
from IPython import embed
from flask_cors import CORS
app = Flask(__name__)

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
    bdg.train(getDataTraining(version))

@app.route('/eval')
def eval():
    version = request.args.get('version')
    bdg.eval(getData(version))

@app.route('/del')
def delete():
    return 0

@app.route('/threed')
def threed():
    return 0

app.run(host='0.0.0.0', port=5000, debug=True)
