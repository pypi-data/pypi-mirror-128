from pymongo.operations import InsertOne, UpdateOne, UpdateMany

class BulkOperationBuilder(object):
    def __init__(self):
        self.requests = []

    def insert_one(self):
        pass

    def update_one(self, filter, update, upsert):
        self.requests.append(UpdateOne(filter, update, upsert))

    def build(self):
        return self.requests