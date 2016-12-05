from django.http import HttpResponse

from credentials import TOKEN

from api import process

def index(request):
    return HttpResponse("Hello stranger. Jazz greets you.")

def api(req, token):
	if token == TOKEN:
		try:
			result = process(req)
			return HttpResponse(result)
		except Exception as err:
			return HttpResponse('Ooops')
	else:
		return HttpResponse('Access granted' if token == TOKEN else 'Go away')