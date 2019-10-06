import time
import os
import json
from IPython import embed
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from helpers import *
from bridge import train



cred = credentials.Certificate("../service-account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()



while True:
	docs = db.collection(u'train').stream()

	for doc in docs:
		exp = doc.id
		data = doc.to_dict()
		print(u'{} => {}'.format(exp, data))
		cleanData = getDataTraining(data)
		train(cleanData)
		docs = db.collection(u'train').document(u'{}'.format(exp)).delete()
		db.collection(u'envs').document(data['version']).set(data)
		break
	time.sleep(30)
