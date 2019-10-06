import os
import json
from IPython import embed
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Listener:
    def __init__(self):
        self.cred = credentials.Certificate("../service-account.json")
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.listener = self.db.collection(u'train')


    def on_snapshot(self, doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(doc.id, doc.to_dict())

    def subscribe(self):
        self.doc_watch = self.listener.on_snapshot(self.on_snapshot)

    def unsubscribe(self):
        embed()





training = Listener()
training.subscribe()

embed()
