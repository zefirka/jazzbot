import os
import re

from json import loads

import bobot
from bobot import Text, Rule

from jazz.credentials import TOKEN

URL = 'https://api.telegram.org/bot{token}/{method}'
CHIRUNO_STICKER = 'BQADAgADvgADzHD_Aieg-50xIfcAAQI'
JAZZ_STICKER = 'BQADAgADBQADIyIEBsnMqhlT3UvLAg'
WEBHOOK = 'https://jazzjail.herokuapp.com/api/{token}/'.format(token=TOKEN)

bot = bobot.init(TOKEN)

def Sticker(sid):
	return {
		'sticker': {
			'sticker': sid
		}
	}

# Rules
jazzRule = Rule({
	'match': [
		re.compile(r'^/catch(@jazzjail_bot)?$', re.I),
		re.compile(r'лови джаза', re.I)
	],
	'response': [
		Text('Я ловлю Джаза'),
		Sticker(CHIRUNO_STICKER),
		Text('Ха-ха, смотрите какой он недовольный!'),
		Sticker(JAZZ_STICKER)
	]
})

sniegRule = Rule({
	'match': [
		re.compile(r'^gdzie jest [sś]nieg\??$', re.I),
		re.compile(r'/gdziesnieg(@jazzjail_bot)?$')
	],
	'response': Text('nie ma.')
})

bakaRule = Rule({
	'match': [
		'baka!',
		'бака!'
	],
	'response': Text('Сам {text}', interpolate=True)
})

fixRule = Rule({
	'match': 'починись плес',
	'response': {
		'keyboard': {
			'resize': True,
			'text': 'Как скажешь, босс!',
			'keyboard': [['Ок, бро.']],
			'autohide': True
		}
	}
})

rules = [
	jazzRule,
	sniegRule,
	bakaRule,
	fixRule,
]

def initialize():
	setup = loads(bot.setWebhook(WEBHOOK))
	
	if setup and setup.get('ok'):
		print('Webhook setted up successfully')
	else:
		print('Error while setting webhook')

	bot.rule(rules)
	return None


# Calls when request recieved
def process(req):
	body = req.body;

	if isinstance(body, bytes):
		body = body.decode('utf-8')

	body = loads(body)

	if os.environ.get('DEBUG') == 'True':
		print(body)

	bot.process(body)
