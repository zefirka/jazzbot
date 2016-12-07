from django.http import HttpResponse
from json import loads, dumps

from random import randint

from jazz.secrets import ABSOLUTE_TOTAL_ADMINS

tokens = {
	
}


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

def isValidLogin(u, p):
	for admin in ABSOLUTE_TOTAL_ADMINS:
		au = admin.get('u')
		ap = admin.get('p')
		if au == u and ap == p:
			return True

	return False


def login(request):
	body = loads(request.body.decode('utf-8'))

	username = body.get('username')
	pwd = body.get('password')
	token = body.get('token')

	users = read()

	if token:
		for admin in tokens:
			if token == tokens[admin]:
				res = dumps({
					'ok': True,
					'users': users,
					'token': token,
					'username': admin
				})
				return HttpResponse(res)
		return HttpResponse(dumps({
			'ok': False
		}))
	elif isValidLogin(username, pwd):
		tokens[username] = genToken()

		res = dumps({
			'ok': True,
			'token': tokens.get(username),
			'users': users
		})
		return HttpResponse(res)
	else:
		return HttpResponse(dumps({'ok': False, 'error': 'Wrong password'}))

def signOut(request):
	body = loads(request.body.decode('utf-8'))
	username = body.get('username')

	if tokens.get(username):
		del token[username]

	return HttpResponse(dumps({'ok': True}))

def add(request):
	body = loads(request.body.decode('utf-8'))
	username = body.get('username')
	userid = body.get('userid')
	token = body.get('token')
	admin = body.get('admin')

	if token == tokens.get(admin):
		users = addUser({
			'username': username,
			'userid': userid
		})

		res = dumps({
			'ok': token == tokens.get(admin),
			'users': users
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

	if token == tokens.get(admin):
		users = removeUser({
			'username': username,
			'userid': userid
		})

		res = dumps({
			'ok': token == tokens.get(admin),
			'users': users
		})
	else:
		res = dumps({
			'ok': False,
			'Error': 'Unathorized request'
		})

	return HttpResponse(res)


def genToken():
	return ''.join(list(map(lambda x: str(randint(0, 1000)), list(range(10)))))