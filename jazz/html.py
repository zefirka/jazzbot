def compile(tag):
    if isinstance(tag, Tag):
        return tag.val()
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
        self.name = name
        self.content = content
        self.attrs = attrs.copy()
        self.attrs.update(kvargs)

    def val(self):
        content = self.content
        attrs = getAttrs(self.attrs.copy())

        if isinstance(content, list):
            content = '\n'.join(list(map(compile, content)))
        elif isinstance(content, Tag):
            content = content.val()

        return '<{0.name} {1} >{2}</{0.name}>'.format(self, attrs, content)

class SimpleTag(Tag):
    def val(self):
        attrs = getAttrs(self.attrs)
        return '<{0.name} {1} />'.format(self, attrs)

def tag(name):
    def createTag(content='', attrs={}, **kvargs):
        attrs.update(kvargs)
        return Tag(name, content, attrs)

    def createSimpleTag(attrs={}, **kvargs):
        attrs.update(kvargs)
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
    Hr,
    P,
    Strong,
    Title,
    Input,
    Button,
    Form,
    Span
] = map(tag, [
    'html',
    'head',
    'script',
    'body',
    'div',
    'h1',
    ['hr'],
    'p',
    'strong',
    'title',
    ['input'],
    'button',
    'form',
    'span'
])

def html5(heading, content):
    return Html([
        Head(heading),
        Body(content)
    ]).val()

def A(content, href, target=None):
    return Tag('a', content, href=href, target=target)

def Css(href, attrs={}):
    attrs['href'] = href
    attrs['rel'] = 'stylesheet'
    return Tag('link', '', attrs)
