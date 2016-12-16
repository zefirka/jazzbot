import os
import re

from json import loads, dumps

from pymongo import MongoClient

import bobot
from bobot import Text, Rule, Sticker, Keyboard

from jazz.utils.auth import isValidHoster
from jazz.secrets import TOKEN, ADMIN, PWD
from jazz.db import get

URL = 'https://api.telegram.org/bot{token}/{method}'
WEBHOOK = 'https://jazzjail.herokuapp.com/api/{token}/'.format(token=TOKEN)

# Environment
bot = bobot.init(TOKEN, 'JazzJail_bot')

owners = []
rules = []
hosters = []

def update(*args):
	global rules, owners, hosters

	owners = get('owners')
	hosters = get('hosters')
	rules = list(map(createRule, get('rules')))

actions = {
	'update': update
}

def getResponse(response):
	if isinstance(response, list):
		return list(map(getResponse, response))
	elif isinstance(response, dict):
		if response.get('type') == 'sticker':
			return Sticker(response.get('body'))
	else:
		return response

def createRule(rule):
	match = rule.get('match', None)
	result = match

	if not match:
		raise Exception('No match in rule {._id}'.format(rule))

	if isinstance(match, dict):
		if match.get('type') == 're':
			flags = {
				'I': 2,
				'L': 4,
				'M': 8
			}
			body = match.get('body')
			result = re.compile(r'' + body.get('text'), flags.get(body.get('flags')))

	desctiption = {
		'match': result,
		'response': getResponse(rule.get('response'))
	}

	if rule.get('action'):
		desctiption['action'] = actions.get(rule.get('action'))

	if rule.get('command'):
		desctiption['command'] = rule.get('command')
	
	return Rule(desctiption)

def initialize():
	setup = loads(bot.setWebhook(WEBHOOK))
	
	if setup and setup.get('ok'):
		print('Webhook setted up successfully')
	else:
		print('Error while setting webhook')

	update()
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

	if isValidHoster(body, hosters):
		bot.process(body)
	else:
		bot.sendMessage(body.get('message').get('from').get('id'), 'You are not allowed to use this bot')
