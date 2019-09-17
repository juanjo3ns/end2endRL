import os
import json
from IPython import embed
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


cred = credentials.Certificate("../../service-account.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'end2endrl.appspot.com'
})

bucket = storage.bucket()

path = '/data/src/templates/csvdata/'

for alg in os.listdir(path):
    for version in os.listdir(os.path.join(path, alg)):
        for agent in os.listdir(os.path.join(path, alg, version)):
            for folder in os.listdir(os.path.join(path, alg, version, agent)):
                for file in os.listdir(os.path.join(path, alg, version, agent, folder)):
                    print(os.path.join(path, alg, version, agent, folder, file))
                    blob = bucket.blob(os.path.join(alg, version, agent, folder, file))
                    print("blob: ", blob)
                    blob.upload_from_filename(os.path.join(path, alg, version, agent, folder, file))
