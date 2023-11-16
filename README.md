# Artemis - Automated Social Engineering Tool
#### Version 1.0 - Released June 2021

Developed by: **Rezi Gelenidze**
GitHub Repository: [Artemis](https://github.com/rezi-gelenidze/artemis)

## Description
Artemis is an advanced social engineering tool that automates phishing operations with ease and flexibility. It enables users to tunnel phishing templates securely via HTTPS using ngrok, capturing critical information like user IP addresses, browser types, and social network credentials. Artemis comes equipped with cloned templates of popular social networks (Facebook, Messenger, Instagram, etc.) and offers a robust template management system to add, remove, and analyze templates.

### Features
- **Secure Tunneling**: Utilize ngrok for HTTPS tunneling of phishing templates.
- **Information Capture**: Efficiently capture user details and credentials.
- **Template Management**: In-built system for managing and customizing phishing templates.
- **Static File Support**: Seamlessly integrate static files or use CDN for template creation.

### Disclaimer
Artemis is developed for **EDUCATIONAL PURPOSES ONLY**. Any illegal use of this tool is strictly prohibited, and the developer assumes no responsibility for misuse or criminal charges resulting from improper use. Users are responsible for adhering to their local laws and regulations.

## Requirements
- Python 3 (Interpreter)
- Ngrok (Executable for HTTPS tunneling)

### Required Python Modules
- Django (For server functionality)
- Whitenoise (Static file management)

Artemis automatically installs all necessary files and libraries (except Python 3).

## Commands

### `-h | --help`
Outputs help text.
```
$ python3 artemis.py -h
```

### `-l | --list [TEMPLATE_NAME]`
Lists installed templates. Details a specific template if `TEMPLATE_NAME` is provided.
```
$ python3 artemis.py -l
$ python3 artemis.py -l facebook
```

### `-r | --remove [TEMPLATE_NAME]`
Removes a specified template after confirmation.
```
$ python3 artemis.py -r facebook
```

### `-d | --deploy [--replace]`
Deploys static files for the Django web server. Use `--replace` to remove old files.
```
$ python3 artemis.py -d
$ python3 artemis.py -d --replace
```

### `-a | --add [TEMPLATE_PATH]`
Adds a new template from a specified path.
```
$ python3 artemis.py -a /home/user/Desktop/my_template
```

### Adding a New Template
Ensure the new template adheres to the specified filesystem for seamless integration.

#### Supported Media Files:
- Images: png, gif, jpeg/jpg, webp, svg, ico, bmp
- Video: mp4, ogv, mov, webm
- Audio: m4a, mp3, wav, aac, ogg
- Fonts: ttf
