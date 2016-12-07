from django.http import HttpResponse

from jazz.secrets import TOKEN

from jazz.api import process
from jazz.html import *


commonHead = [
    Css('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'),
    Css('/static/index.css'),
    Title('JazzBot :: Hello stranger, Jazz greets you!'),
    Js('https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js'),
    Js('/static/jquery.cookie-1.4.1.min.js'),
    Js('/static/index.js')
]

def container(x):
    return Div(x, className='container')

def index(request):
    page = html5(commonHead, container([
        H1("Hello stranger. Jazz greets you."),
        Hr(),
        A('Adm†nka ejje', '/admin')
    ]))
    return HttpResponse(page)

def adminka(request):
    page = Div([
        'Allahu',
        Div('Akbar', id="{item}")
    ]).val()

    templates = [
        Template('login', [
            Div([
                    Span([
                    'Hello,',
                    Strong('{username}'),
                    '!'
                ], className='b-login__user'),
                Span('Sign out', className='btn btn-default b-login__sign-out js-out')
            ], className='b-login'),
            Hr()
        ]),
        
        Template('row', Div([
            Input(name='userid', value='{userid}', className='form-control user-info'),
            Input(name='username', value='{username}', className='form-control user-info'),
            Span(className='glyphicon glyphicon-remove js-remove', uid='{userid}')
        ], className="b-content__item", id='{itemId}')),

        Template('controls', Div([
            Hr(),
            Div(
                Span('Add new hoster', className='btn btn-success js-show-add'),
                className='b-admin-control'
            ),
            Div([
                Input(
                    placeholder='Username', 
                    type='text',
                    name='add_username',
                    className='form-control user-info'),
                Span('or', className='user-info-or'),
                Input(
                    placeholder='UserId', 
                    type='text',
                    name='add_userid',
                    className='form-control user-info'),
                Span('Add', className='btn btn-success js-add', token='{token}'),
                Span('Cancel', className='btn btn-danger js-cancel',)
            ], className='b-user-data g-hidden')
        ], className='b-admin-controls'))
    ]

    paranja = Div(Div(SimpleTag('img', src='/static/triangle.svg'), className='spin2'), className='paranja')

    content = container([
        Div([
            H1("Adminka ejje"),
            Hr(),
        ], className='row'),
        Div(className='b-login-wrapper g-hidden row'),
        Div([
            Div([
                Form([
                    Div([
                        Div(
                            Input(
                                placeholder='Username', 
                                type='text',
                                id='username',
                                className='form-control'),
                            className='b-form__field'
                        ),
                        Div(
                            Input(
                                placeholder='Password',
                                type='password',
                                id='password',
                                className='form-control'),
                            className='b-form__field'
                        )
                    ], className="b-form__fieldset"),
                    Div([
                        Label([
                            Span('Remember Me'),
                            Input(id='remember', type='checkbox')
                        ], className="b-form__button-label"),
                        Button('Ok', className="b-form__button btn btn-primary", id='login')
                    ], className="b-form__buttons")
                ], className="b-form col-md-4 col-sm-6 col-xs-12 col-lg-3"),
                Div([
                    Div('', className="b-form__error well well-sm text-danger g-hidden"),
                    SimpleTag('img', src='/static/triangle.svg', className="b-spin b-spin_visible_no")
                ], id='spin', className='right-col col-md-8 col-sm-6 hidden-xs col-lg-9')
            ], className="row"),
            Hr()
        ], className='b-controls row'),
        Div(Div([
            H2('Allowed users'),
            Hr(),
            Div(className='b-table')
        ], className="b-content g-hidden"), className='row'),
        Div(Div(className='b-admin-controls-wrapper'), className='row')
    ])

    page = html5(commonHead, [content, paranja, templates])
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
