# Artemis - automated Social Engineering tool
#### v1.0 release, June 2021

Developer: **Rezi Gelenidze**
Github repository: https://github.com/rezi-gelenidze/artemis

### Description
Artemis provides automated and flexible phishing functionalities,
you can tunnel any template via secured HTTPS with ngrok tunnel,
you are an able to capture user IP address, browser type and social
network credentials, if the user types in tunneled template form 
(ex. user typed his credentials in your fake Facebook login page). Artemis includes
some popular social network cloned fake templates (Facebook, Messenger, Instagram and etc.),
but it also includes template management system for adding a new template, removing existing,
listing installed templates and analyzing existing template directories and files.


### **Disclaimer**
Any actions and/or activities related to using this Artemis social engineering tool is solely your responsibility, this tool is for **EDUCATIONAL PURPOSES ONLY** . The misuse of this tool can result in criminal charges brought against the persons in question. The developer will not be held responsible in the event any criminal charges be brought against any individuals misusing this tool to break the law.


### requirements
- python3 (python interpreter)
- ngrok (ngrok executable for safe https tunneling)

*required python modules:
- django (python web framework for Artemis server functioning)
- whitenoise (static files manager for django web server)
- requests (python library for web requests)

Artemis automatically installs all required files
and libraries if not installed (except python3)


### commands


#### -h | --help

outputs this help text.

`$ python3 artemis.py -h`

#### -l | --list [TEMPLATE_NAME]

outputs list of installed templates. If TEMPLATE_NAME is
present, specific template is analyzed and information is listed.

`$ python3 artemis.py -l`
`$ python3 artemis.py -l facebook`


#### -r | --remove [TEMPLATE_NAME]

command for removing existing template and its files.
Command firstly outputs template details and directories,
and asks user if he really wants to remove template.
If user proceeds, all template static and HTML files are removed.

`$ python3 artemis.py -r facebook`


#### -d | --deploy [--replace]

manual deploying for Django staticfiles.
This command offers automatic deployment of static files
for Django web server (Django uses whitenoise static file manager).
if command is executed Artemis creates folder for deployed staticfiles if not present,
or merges new staticfiles with existing ones. if --replace argument is provided, old staticfiles
folder is deleted and new one is created with new files only (no merging with old files).

`$ python3 artemis.py -d`
`$ python3 artemis.py -d --replace`


#### -a | --add [TEMPLATE_PATH]

initialized new template from given absolute or relative path (TEMPLATE_PATH), checks its
validity and then asks user to provide name for newly created template.
When name is provided, all valid files are copied in Artemis management
directories and newly copied HTML file is modified to support Django templating
language.

`$ python3 artemis.py -a /home/user/Desktop/my_template`

#### New template content

when new template is added, artemis scans it's directory, determines it's validity and tries to copy supported content.
New template must have this filesystem:
* contains at least one HTML file, named `index.html`
* all CSS files are directly stored in `css` directory
* all Javascript files are directly stored in `js` directory
* all media files are directly stored in `media` directory
```
mytemplate/
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
#### supported media files:
* image
	* png
	* gif
	* jpeg/jpg
	* webp
	* svg
	* ico
	* bmp
* video
	* mp4
	* ogv
	* mov
	* webm
* audio
	* m4a
	* mp3
	* wav
	* aac
	* ogg
* fonts
	* ttf 
	

