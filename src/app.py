from flask import Flask, jsonify, request
from helpers import getData, saveData
import bridge as bdg
import json
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'


@app.route('/envs', methods=['GET', 'POST', 'PUT'])
def add():
    if request.method == 'GET':
        version = request.args.get('version')
        return jsonify(getData(version))
    elif request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
        saveData(data)
        # Re-render button environments
        return "Correctly added"


@app.route('/train')
def train():
    version = request.args.get('version')
    bdg.train(getData(version))

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
