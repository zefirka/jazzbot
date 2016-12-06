from django.http import HttpResponse

from jazz.credentials import TOKEN

from jazz.api import process
from jazz.html import *


commonHead = [
    Css('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'),
    Css('index.css'),
    Title('JazzBot :: Hello stranger, Jazz greets you!')
]

def container(x):
    return Div(Div(x, className="row"), className='container')

def index(request):
    page = html5(commonHead, container([
        H1("Hello stranger. Jazz greets you."),
        Hr(),
        A('Adm†nka ejje', '/admin')
    ]))
    return HttpResponse(page)

def adminka(request):
    page = html5(commonHead, container([
        H1("Adminka ejje"),
        Hr(),
        Div(
            Form([
                Div(Input(placeholder='usr')),
                Div(Input(placeholder='pwd', type='password')),
                Div([
                    Span(['REMEMBER MEEE', Input({'type': 'checkbox'})], className="col-md-6 col-sm-6 col-xs-6 col-lg-6"),
                    Span(Button('Ok', className="btn btn-primary"), className="col-md-6 col-sm-6 col-xs-6 col-lg-6")
                ], className="row")
            ])
        , className="col-md-4 col-sm-6 col-xs-8 col-lg-3")
    ]))
    return HttpResponse(page)

def api(req, token):
    if token == TOKEN:
        try:
            result = process(req)
            return HttpResponse(result)
        except Exception as err:
            print(err)
            return HttpResponse('Ooops')
    else:
        return HttpResponse('Go away')
