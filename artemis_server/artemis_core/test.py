import re

LINK_RE = r'''<[^>]*(?:src|href)\s*=\s*((?:'|")(?:(?:media|css|js)(?:\/|\\)[a-zA-Z0-9\-\?\/\\.\s]+)(?:'|"))[^<]*>'''

content = '<link rel="stylesheet" href="css/navbar.css"> <img class=\'nav-logo\' src="media/aslolgsdg">'


def replace(text):
    path = text.group(1)

    print(path)

    return text.group().replace(path ,"'{% static" + f' {path} ' + "%}'")

# process HTML content
x = re.sub(LINK_RE, replace, content)

print('FINAL', x)