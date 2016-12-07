def compile(tag):
    if isinstance(tag, Tag):
        return tag.val()

    if isinstance(tag, list):
        return '\n'.join(list(map(compile, tag.copy())))
    
    return tag

def getAttrs(attrs):
    if not attrs:
        return ''

    res = ''

    for attr in attrs:
        if attrs[attr]:
            attrName = 'class' if attr == 'className' else attr
            res += '{attrName}="{attrVal}" '.format(attrName=attrName, attrVal=attrs[attr])
    return res

class Tag():
    def __init__(self, name, content='', attrs={}, **kvargs):
        # print('Attrs on {0} and content {1} '.format(name, content))
        # print(attrs)

        self.name = name
        self.content = content
        self.attrs = attrs.copy()
        self.attrs.update(kvargs.copy())

        # print(content)
        # print(attrs)

    def val(self):
        content = compile(self.content)
        attrs = getAttrs(self.attrs)

        # print(attrs)

        return '<{0.name} {1} >{2}</{0.name}>'.format(self, attrs, content)

class SimpleTag(Tag):
    def val(self):
        attrs = getAttrs(self.attrs)
        return '<{0.name} {1} />'.format(self, attrs)

def tag(name):
    def createTag(content='', attrs={}, **kvargs):
        # print('Creating tag {0} with attrs = {1}, and kvargs = {2}'.format(name, attrs, kvargs))
        attrs = attrs.copy()
        attrs.update(kvargs.copy())
        return Tag(name, content, attrs)

    def createSimpleTag(attrs={}, **kvargs):
        attrs = attrs.copy()
        attrs.update(kvargs.copy())
        return SimpleTag(name[0], '', attrs)

    if isinstance(name, list):
        return createSimpleTag
    return createTag

[
    Html,
    Head,
    Script,
    Body,
    Div,
    H1,
    H2,
    H3,
    Hr,
    P,
    Strong,
    Title,
    Input,
    Button,
    Form,
    Span,
    Label
] = map(tag, [
    'html',
    'head',
    'script',
    'body',
    'div',
    'h1', 'h2', 'h3',
    ['hr'],
    'p',
    'strong',
    'title',
    ['input'],
    'button',
    'form',
    'span',
    'label'
])

def html5(heading, content):
    return Html([
        Head(heading),
        Body(content)
    ]).val()

def A(content, href, target=None):
    return Tag('a', content, href=href, target=target)

def Css(href, attrs={}):
    attrs = attrs.copy()
    attrs['href'] = href
    attrs['rel'] = 'stylesheet'
    return SimpleTag('link', '', attrs)

def Js(src, attrs={}):
    attrs = attrs.copy()
    attrs['src'] = src
    attrs['type'] = 'text/javascript'
    return Tag('script', '', attrs)

def Template(name, content):
    return Tag('script', content, id='tpl__'+name, type='template')
