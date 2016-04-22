# coding=utf-8

import json
import re

from credentials import TOKEN
from call import get

URL = 'https://api.telegram.org/bot{token}/{method}'
CHIRUNO_STICKER = 'BQADAgADvgADzHD_Aieg-50xIfcAAQI'
JAZZ_STICKER = 'BQADAgADBQADIyIEBsnMqhlT3UvLAg'
WEBHOOK = 'https://jazzjail.herokuapp.com/api/{token}/'.format(token=TOKEN)

def print_jazz_status(status):
	if status:
		print 'Jazz was sended successfully' 
	else: 
		print 'An error was occured'

def send_jazz(message):
	id = message.get('chat').get('id')
	print id
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

def send(text):
	def send_message(message):
		id = message.get('chat').get('id')

		return get(method('sendMessage'), {
			'chat_id': id,
			'text': text
		})
	return send_message

def equals(text):
	return lambda recieved_text: text == recieved_text

#################################
# ACTIONS DICT
actions = {
	'jazz': {
		'match': equals('лови джаза'.decode('utf-8')),
		'action': send_jazz,
		'after': print_jazz_status
	},
	'sneg': {
		'match': lambda text: re.match(re.compile(r'^gdzie jest [sś]nieg\??$'.decode('utf-8')), text),
		'action': send('nie ma.')
	},
	'hello': {
		'match': equals('baka!'),
		'action': send('я не бака')
	}
}

#################################
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


# Calls when request recieved
def process(req):
	message = json.loads(req.body, encoding='utf-8').get('message', None)
	text = message.get('text').lower()

	for action_name in actions:
		match = actions.get(action_name).get('match')
		action = actions.get(action_name).get('action')
		after = actions.get(action_name).get('after')
		print text
		print match(text);
		if (match(text)):
			result = action(message)
			if (after):
				after(result)
				return True

## Helpers
def method(m):
	return URL.format(token=TOKEN, method=m)

def setWebhook(url):
	return get(method('setWebhook'), {
		'url': url
	})