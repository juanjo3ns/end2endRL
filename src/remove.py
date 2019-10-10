import os
import sys
import json
from IPython import embed
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import copy
import shutil


version = sys.argv[1]
alg = version.split('.')[0]


cred = credentials.Certificate("../service-account.json")
firebase_admin.initialize_app(cred, {
	'storageBucket': 'end2endrl.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()

# DELETE CSV DATA FROM FIREBASE STORAGE
try:
	blobs = bucket.list_blobs(prefix=os.path.join(alg, version))
	for blob in blobs:
	  blob.delete()
	print("CSV data deleted from firebase storage...")
except:
	pass

# DELETE JSON ENVIRONMENTS FROM FIREBASE
try:
	docs = db.collection(u'envs').document(u'{}'.format(version)).delete()
	print("JSON envs deleted from firestore...")
except:
	pass

path_container = '/data/src/templates/csvdata/'
path_tensorboard = '/data/src/tensorboard/'
path_weights = '/data/src/weights/'


# DELETE LOGS, CSVS AND WEIGHTS FROM LOCAL SERVER
try:
	shutil.rmtree(os.path.join(path_container, alg, version))
	shutil.rmtree(os.path.join(path_tensorboard, alg, version))
	shutil.rmtree(os.path.join(path_weights, alg, version))
	print("Deleted files from local server...")
except:
	pass
