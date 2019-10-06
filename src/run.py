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



cred = credentials.Certificate("../service-account.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'end2endrl.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()

path = '/data/src/templates/csvdata/'

def uploadFiles(alg, version):
	for agent in os.listdir(os.path.join(path, alg, version)):
		for folder in os.listdir(os.path.join(path, alg, version, agent)):
			for file in os.listdir(os.path.join(path, alg, version, agent, folder)):
				print(os.path.join(path, alg, version, agent, folder, file))
				blob = bucket.blob(os.path.join(alg, version, agent, folder, file))
				print("blob: ", blob)
				blob.upload_from_filename(os.path.join(path, alg, version, agent, folder, file))



while True:
	docs = db.collection(u'train').stream()

	for doc in docs:
		exp = doc.id
		data = doc.to_dict()
		print(u'{} => {}'.format(exp, data))
		cleanData = getDataTraining(data)
		bridge.train(cleanData)
		bridge.eval(cleanData)
		uploadFiles(data['alg'], data['version'])
		docs = db.collection(u'train').document(u'{}'.format(exp)).delete()
		db.collection(u'envs').document(data['version']).set(data)
		break
	time.sleep(30)
