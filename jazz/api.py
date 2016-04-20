# coding=utf-8

import requests
import json

from credentials import TOKEN

URL = 'https://api.telegram.org/bot{token}/{method}'
CHIRUNO_STICKER = 'BQADAgADvgADzHD_Aieg-50xIfcAAQI'
JAZZ_STICKER = 'BQADAgADBQADIyIEBsnMqhlT3UvLAg'
WEBHOOK = 'https://jazzjail.herokuapp.com/api/{token}/'.format(token=TOKEN)

def method(m):
	return URL.format(token=TOKEN, method=m)

# Will containt setWebhook
def initialize():
	auth = get(method('getMe'))
	
	if (auth.get('ok') is True):
		setup = setWebhook(WEBHOOK)
		
		if (setup.get('ok')):
			print 'Webhook setted up successfully'
		else:
			print 'Error'
	else:
		print 'error';


def setWebhook(url):
	return get(method('setWebhook'), {
		'url': url
	})

def process(req):
	message = json.loads(req.body, encoding='utf-8').get('message', None)
	
	if (message.get('text') == 'Лови Джаза'.decode('utf-8')):
		send = send_jazz(message.get('chat').get('id'))

		if (send):
			print 'Jazz was sended successfully'
		else:
			print 'An error occured while Jazz sending'

def call(url, method='GET', data={}, headers={}):
	if method is 'GET':
		req = requests.get(url, params=data, headers={})
	else:
		req = requests.post(url, data=json.dumps(data), headers={})
	
	req.encoding = 'utf-8'

	return json.loads(req.text) if req and req.text else None


def get(url, data={}):
    return call(url, 'GET', data)

def post(url, data={}):
    return call(url, 'POST', data)

def send_jazz(id):
	reqs = [
		get(method('sendMessage'), {
			'chat_id': id,
			'text': 'Я ловлю Джаза'
		}),
		get(method('sendSticker'), {
			'chat_id': id,
			'sticker': CHIRUNO_STICKER
		}),
		get(method('sendMessage'), {
			'chat_id': id,
			'text': 'Ха-ха, смотрите какой он недовольный!'
		}),
		get(method('sendSticker'), {
			'chat_id': id,
			'sticker': JAZZ_STICKER
		})
	]

	return len(filter(lambda req: req.get('ok') != True, reqs)) == 0


def process(req):
	message = json.loads(req.body, encoding='utf-8').get('message', None)
	
	if (message.get('text') == 'gdzie jest śnieg?'.decode('utf-8')):
		send = send_jazz(message.get('chat').get('id'))

		if (send):
			print 'Jazz was sended successfully'
		else:
			print 'An error occured while Jazz sending'

def call(url, method='GET', data={}, headers={}):
	if method is 'GET':
		req = requests.get(url, params=data, headers={})
	else:
		req = requests.post(url, data=json.dumps(data), headers={})
	
	req.encoding = 'utf-8'

	return json.loads(req.text) if req and req.text else None


def get(url, data={}):
    return call(url, 'GET', data)

def post(url, data={}):
    return call(url, 'POST', data)

def send_jazz(id):
	reqs = [
		get(method('sendMessage'), {
			'chat_id': id,
			'text': 'nie ma.'
		})
	]

	return len(filter(lambda req: req.get('ok') != True, reqs)) == 0
