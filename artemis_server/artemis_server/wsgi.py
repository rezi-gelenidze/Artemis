"""
WSGI config for artemis_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artemis_server.settings')

application = get_wsgi_application()


from artemis_core import utils

# clear console from django default header text
utils.remove_prev_lines(7)

print('Send this to your target:', utils.colorize('orange', os.environ.get('ARTEMIS_URL', 'URL not found...')))

print('\nWaiting for targets...\n')
