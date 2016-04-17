# coding=utf-8

import requests
import json

from credentials import TOKEN

URL = 'https://api.telegram.org/bot{token}/{method}'

CHIRUNO_STICKER = 'BQADAgADvgADzHD_Aieg-50xIfcAAQI'
JAZZ_STICKER = 'BQADAgADBQADIyIEBsnMqhlT3UvLAg'

def method(m):
	return URL.format(token=TOKEN, method=m)

def initialize():
	auth = get(method('getMe'))
	
	if (auth.get('ok') is True):
		updates = get(method('getUpdates'))
		last_chat_id = updates.get('result').pop().get('message').get('chat').get('id')
		
		reqs = send_jazz(last_chat_id)
		
		if (reqs):
			print 'All requests sent successfully'
		else:
			print 'Some req failed'
	else:
		print 'Атятят'



	return False


def call(url, method='GET', data={}, headers={}):
	if method is 'GET':
		req = requests.get(url, params=data, headers={})
	else:
		req = requests.post(url, data=json.dumps(data), headers={})
	
	req.encoding = 'utf-8'

	return json.loads(req.text)


def get(url, data={}, headers={}):
    return call(url, 'GET', data, headers)

def post(url, data={}, headers={}):
    return call(url, 'POST', data, {
		'Content-Type' : 'application/json' 
    })

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
