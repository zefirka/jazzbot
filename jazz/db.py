from pymongo import MongoClient
from jazz.secrets import TOKEN, ADMIN, PWD

URL = 'https://api.telegram.org/bot{token}/{method}'
DBURL = 'mongodb://{admin}:{pwd}@ds119568.mlab.com:19568/jazzbot'.format(admin=ADMIN, pwd=PWD)

dbClient = MongoClient(DBURL)
db = dbClient.get_default_database()

def get(collection):
	return list(map(removeId, list(db[collection].find())))

def insert(collection, item):
	return db['collection'].insert_one(item)

def removeId(item):
	del item['_id']
	return item

def setTokenFor():
	pass