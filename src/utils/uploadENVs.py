import os
import json
from IPython import embed
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("../../service-account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


envs_path = '/data/envs'
for version in os.listdir(envs_path):
	with open(os.path.join(envs_path, version), 'r') as f:
		raw_data = json.load(f)
		db.collection(u'envs').document(version.split('.json')[0]).set(raw_data)
