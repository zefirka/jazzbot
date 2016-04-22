import json
import requests

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