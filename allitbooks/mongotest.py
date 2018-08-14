from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['test']

collection = db['inventory']

print(type(collection))

print(collection.find_one())

