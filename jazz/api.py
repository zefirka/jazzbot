import os
import re

from json import loads, dumps

import bobot
from bobot import Text, Rule, Sticker, Keyboard

from jazz.secrets import TOKEN

URL = 'https://api.telegram.org/bot{token}/{method}'
CHIRUNO_STICKER = 'BQADAgADvgADzHD_Aieg-50xIfcAAQI'
JAZZ_STICKER = 'BQADAgADBQADIyIEBsnMqhlT3UvLAg'
WEBHOOK = 'https://jazzjail.herokuapp.com/api/{token}/'.format(token=TOKEN)

bot = bobot.init(TOKEN, 'JazzJail_bot')

# Rules
jazzRule = Rule({
	'match': re.compile(r'лови джаза', re.I),
	'command': 'catch',
	'response': [
		Text('Я ловлю Джаза'),
		Sticker(CHIRUNO_STICKER),
		Text('Ха-ха, смотрите какой он недовольный!'),
		Sticker(JAZZ_STICKER)
	]
})

sniegRule = Rule({
	'match': re.compile(r'^gdzie jest [sś]nieg\??$', re.I),
	'command': 'gdziesnieg',
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
	'response': Text('корошо', markup=dumps({'remove_keyboard': True}))
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
