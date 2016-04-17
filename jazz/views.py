from django.http import HttpResponse

from credentials import TOKEN

def index(request):
    return HttpResponse("Hello stranger. Jazz greets you.")

def api(req, token):
	return HttpResponse('Access granted' if token == TOKEN else 'Fuck off')