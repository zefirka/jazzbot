from django.http import HttpResponse
from json import loads, dumps

from random import randint

from jazz.db import get, setTokenFor, addNewHoster, removeHoster

def read():
    with open('jazz/data/users.json', 'r') as jsonfile:
        content = jsonfile.read()
        return loads(content)

def write(data):
    with open('jazz/data/users.json', 'w+') as jsonfile:
        content = dumps(data)
        jsonfile.write(content)

def addUser(user):
	users = read()
	users.append(user)
	write(users)
	return users

def removeUser(u):
	users = read()
	
	res = []

	for user in users:
		n = user.get('username')
		i = user.get('userid')
		print(n, i, u)
		if n != u.get('username') and i != u.get('userid'):
			res.append(user)

	write(res)
	return res

def isValidLogin(username, pwd, token=''):
	owners = get('owners')
	
	for owner in owners:
		au = owner.get('username')
		ap = owner.get('password')
		at = owner.get('token')

		if (au == username and ap == pwd) or token == at:
			return {
				'valid': True,
				'token': owner.get('token'),
				'username': au
			}

	return {
		'valid': False
	}


def login(request):
	body = loads(request.body.decode('utf-8'))

	username = body.get('username')
	pwd = body.get('password')
	token = body.get('token')

	credentials = isValidLogin(username, pwd, token)

	if credentials.get('valid'):
		sendedToken = token
		credentialsToken = credentials.get('token')

		if not (sendedToken == credentialsToken and credentialsToken != None):
			token = genToken()
			setTokenFor(username, token)
		else:
			token = sendedToken or credentialsToken
			setTokenFor(username, None)
		print(credentials)
		res = dumps({
			'ok': True,
			'users': get('hosters'),
			'token': token,
			'username': username or credentials.get('username')
		})
	else:
		res = dumps({'ok': False, 'error': 'Wrong password'})

	return HttpResponse(res)

# {username, [token]} -> {ok}
def signOut(request):
	body = loads(request.body.decode('utf-8'))
	username = body.get('username')
	token = body.get('username')
	setTokenFor(username, None)
	return HttpResponse(dumps({'ok': True}))


def add(request):
	body = loads(request.body.decode('utf-8'))
	username = body.get('username')
	userid = body.get('userid')
	
	token = body.get('token')
	admin = body.get('admin')


	if isValidLogin(None, None, token):
		hosters = addNewHoster({
			'username': username,
			'userid': userid
		})

		res = dumps({
			'ok': True,
			'users': hosters
		})
	else:
		res = dumps({
			'ok': False,
			'Error': 'Unathorized request'
		})

	return HttpResponse(res)

def remove(request):
	body = loads(request.body.decode('utf-8'))
	username = body.get('username')
	userid = body.get('userid')
	
	token = body.get('token')
	admin = body.get('admin')


	if isValidLogin(None, None, token):
		hosters = removeHoster({
			'username': username,
			'userid': userid
		})

		res = dumps({
			'ok': True,
			'users': hosters
		})
	else:
		res = dumps({
			'ok': False,
			'Error': 'Unathorized request'
		})

	return HttpResponse(res)


def genToken():
	return ''.join(list(map(lambda x: str(randint(0, 1000)), list(range(10)))))