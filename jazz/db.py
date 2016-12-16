from pymongo import MongoClient
from jazz.secrets import TOKEN, ADMIN, PWD

URL = 'https://api.telegram.org/bot{token}/{method}'
DBURL = 'mongodb://{admin}:{pwd}@ds119568.mlab.com:19568/jazzbot'.format(admin=ADMIN, pwd=PWD)

dbClient = MongoClient(DBURL)
db = dbClient.get_default_database()

def get(collection):
	return list(map(removeId, list(db[collection].find())))

def insert(collection, item):
	return db[collection].insert_one(item)

def remove(collection, item):
	return db[collection].delete_one(item)

def removeId(item):
	del item['_id']
	return item

def setTokenFor(username, token):
	return db.owners.update({
		'username': username
	}, {
		'$set': {
			'token': token
		}
	})

def addNewHoster(hoster):
	insert('hosters', hoster)
	return get('hosters')

def removeHoster(hoster):
	remove('hosters', hoster)
	return get('hosters')