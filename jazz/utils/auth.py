def isValidHoster(update, hosters):
	uid = None
	uname = None
	try:
		message = update.get('message')
		uid = message.get('from').get('id')
		uname = message.get('from').get('username')
	except Exception as error:
		print(error)

	for hoster in hosters:
		hu = hoster.get('username')
		hi = hoster.get('userid')
		
		if hu == uname or hi == uid:
			print('allowrd')
			return True

	return False
