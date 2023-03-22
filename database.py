import pymongo
import certifi

class DBReader:
    def __init__(self, link):
        self.link = link
        client = pymongo.MongoClient(self.link, tlsCAFile=certifi.where())
        db = client["bank"]
        self.collection = db["clients"]

    def read(self, filter):
        all_data = self.collection.find(filter)
        return all_data

    def find_one(self, filter):
        return self.collection.find_one(filter)

class DBWriter:
    def __init__(self, link):
        client = pymongo.MongoClient(link, tlsCAFile=certifi.where())
        db = client["bank"]
        self.collection = db["clients"]

    def write(self, value):
        self.collection.insert(value)

    def insert_one(self, value):
        self.collection.insert_one(value)

    def update(self, filter, value):
        self.collection.update_many(filter, value)