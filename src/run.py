import time
import os
import json
from IPython import embed
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from helpers import *
import bridge
import pysftp
import copy


cred = credentials.Certificate("../service-account.json")
firebase_admin.initialize_app(cred, {
	'storageBucket': 'end2endrl.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()

path_container = '/data/src/templates/csvdata/'
path_aws = '/home/ubuntu/tensorboard/logs/'
path_tensorboard = '/data/src/tensorboard/'

def uploadFiles(alg, version):
	for agent in os.listdir(os.path.join(path_container, alg, version)):
		for folder in os.listdir(os.path.join(path_container, alg, version, agent)):
			for file in os.listdir(os.path.join(path_container, alg, version, agent, folder)):
				print(os.path.join(path_container, alg, version, agent, folder, file))
				blob = bucket.blob(os.path.join(alg, version, agent, folder, file))
				print("blob: ", blob)
				blob.upload_from_filename(os.path.join(path_container, alg, version, agent, folder, file))

def uploadLogs(alg, version):
	cnopts = pysftp.CnOpts()
	cnopts.hostkeys = None
	sftp = pysftp.Connection(os.environ['AWS_IP'], username='ubuntu', private_key="/data/tensorboard.pem", cnopts=cnopts)
	sftp.mkdir(os.path.join(path_aws,'{}'.format(alg), '{}'.format(version)))
	with sftp.cd(os.path.join(path_aws,'{}'.format(alg), '{}'.format(version))):
		sftp.put_r(os.path.join(path_tensorboard, '{}'.format(alg), '{}'.format(version)), './')
	sftp.close()



while True:
	docs = db.collection(u'train').stream()
	for doc in docs:
		exp = doc.id
		data = doc.to_dict()
		print(u'{} => {}'.format(exp, data))
		cleanData = getDataTraining(data)
		bridge.train(copy.deepcopy(cleanData))
		bridge.eval(copy.deepcopy(cleanData))
		uploadFiles(data['alg'], data['version'])
		# uploadLogs(data['alg'], data['version'])
		docs = db.collection(u'train').document(u'{}'.format(exp)).delete()
		db.collection(u'envs').document(data['version']).set(data)
		break
	time.sleep(30)
