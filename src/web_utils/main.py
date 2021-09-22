import argparse
import json
import os
import subprocess
import sys


def sys_argv():
    return sys.argv


def init_argparse(args: list):
    parser = argparse.ArgumentParser(
        description="Web app create utility. It can create FastAPI, Django," +
        " Flask and Pyramid apps with good folder structure automatically." +
        " Please make sure that pip is working and is " +
        "callable py typing 'pip' for this to work")

    parser.add_argument(
        "command", help="Command to be executed", choices=['create'])
    parser.add_argument("app_name", help="App name to be given",)
    parser.add_argument("-dr", "--dir_name",
                        help="Specify a folder name.", default='[cwd]')
    venv_name = parser.add_mutually_exclusive_group(required=True)
    venv_name.add_argument("-en", "--venv_name",
                           help="Specify the virtualenv name.")
    venv_name.add_argument(
        "-ne", "--no_venv",
        help="Doesn't include virtualenv", action='store_true')
    app_type = parser.add_mutually_exclusive_group(required=True)
    app_type.add_argument("-fi", "--fastapi",
                          action='store_true', help="Creates a fastapi app")
    app_type.add_argument(
        "-d", "--django", action='store_true', help="Creates a django app")
    app_type.add_argument(
        "-fl", "--flask", action='store_true', help="Creates a flask app")
    app_type.add_argument(
        "-p", "--pyramid", action='store_true', help="Creates a pyramid app")
    app_type.set_defaults(fastapi=False, django=False,
                          flask=False, pyramid=False)
    return parser.parse_args(args)
# radiowaves, microwaves, electromagnet rays


def create_tool(args: argparse.Namespace):
    print("Initializing...")
    if args.dir_name == "[cwd]":
        dir_name = ""
        cd_dir = ''
    else:
        pass
        if os.path.exists(args.dir_name) is not True:
            os.mkdir(args.dir_name)
        else:
            print(
                f"Warning: Directory {args.dir_name} already exists." +
                f" Writing files to {args.dir_name}"
            )
            import time
            time.sleep(3.1)
        dir_name = args.dir_name
        cd_dir = "cd {} &&".format(dir_name)
        print("Initialised")
    if not os.path.exists(os.path.join(dir_name, ".web")):
        print("Preparing files...")
        if args.no_venv is True:
            venv = False
            print("Prepared")
        else:
            print("Prepared\nInstalling virtualenv...")
            subprocess.run("pip install virtualenv", shell=True)
            venv = True
            print("Installed")
        print("Creating .gitignore")
        if args.no_venv is True:
            with open(os.path.join(dir_name, ".gitignore"), "w") as f:
                f.write(".web\n")
                f.write("__pycache__\n")
                f.write('.vscode\n')
                f.write('.idea\n')
                f.write('.mypy_cache\n')
                f.write('*.pyc')
                f.close()
        else:
            with open(os.path.join(dir_name, ".gitignore"), "w") as f:
                f.write(args.venv_name+"\n")
                f.write(".web\n")
                f.write("__pycache__\n")
                f.write('.vscode\n')
                f.write('.idea\n')
                f.write('.mypy_cache\n')
                f.write('*.pyc')
                f.close()
        print("Created .gitignore")
        if sys.platform == 'win32':
            venv_activate = os.path.join(args.venv_name, 'Scripts', 'activate')
        else:
            venv_activate = f"source ./{args.venv_name}/bin/activate"
        print("Prepared files")
        if args.fastapi is True:
            if venv is True:
                print("Creating virtualenv and activating it ...")
                command = f"{cd_dir} virtualenv "
                command = command + f"{args.venv_name} && {venv_activate} &&"
                print("Activated")
            else:
                command = ''
            print("Installing fastapi and uvicorn...")
            subprocess.run(
                f"{command} pip install fastapi uvicorn[standard]", shell=True)
            if dir_name == '':
                dir_name = dir_name
            print("Installed\nCreating {}.py".format(args.app_name))
            with open(os.path.join(dir_name, args.app_name+".py"), "w") as f:
                f.write("""from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def main():
    return "Working" """)
                f.close()
                if venv is True:
                    config_dict = {
                        'framework': 'fastapi',
                        'run_command': f'uvicorn {args.app_name}:app --reload',
                        'venv_name': args.venv_name,
                        'app_name': args.app_name}
                else:
                    config_dict = {
                        'framework': 'fastapi',
                        'run_command': f'uvicorn {args.app_name}:app --reload',
                        'venv_name': None,
                        'app_name': args.app_name}
            print("Created {}.py".format(args.app_name))
        elif args.django is True:
            if venv is True:
                print("Creating virtualenv and activating it ...")
                command = f"{cd_dir} virtualenv "
                command = command + f"{args.venv_name} && {venv_activate} &&"
                config_dict = {
                    'framework': 'django',
                    'run_command': 'python manage.py runserver',
                    'venv_name': args.venv_name,
                    'app_name': args.app_name}
                print("Activated")
            else:
                command = ''
                config_dict = {
                    'framework': 'django',
                    'run_command': 'python manage.py runserver',
                    'venv_name': None,
                    'app_name': args.app_name}
            print("Installing django")
            subprocess.run(f"{command} pip install django", shell=True)
            if dir_name == '':
                pass
            else:
                dir_name = "cd "+dir_name+" &&"
            print("Installed Django\nCreating project")
            subprocess.run(
                "{} ".format(dir_name)
                + "django-admin startproject {} .".format(args.app_name),
                shell=True)
            print("Created project")
        elif args.flask is True:
            if venv is True:
                print("Creating virtualenv and activating it...")
                command = f"{cd_dir} virtualenv "
                command = command + f"{args.venv_name} && {venv_activate} &&"
                config_dict = {
                    'framework': 'flask',
                    'run_command': f'python {args.app_name}.py',
                    'venv_name': args.venv_name,
                    'app_name': args.app_name}
                print("Activated")
            else:
                command = ''
                config_dict = {
                    'framework': 'flask',
                    'run_command': f'python {args.app_name}.py',
                    'venv_name': None,
                    'app_name': args.app_name}
            print("Installing flask...")
            subprocess.run(f"{command} pip install flask", shell=True)
            print("Installed")
            if dir_name == '':
                dir_name = dir_name
            print("Creating {}.py".format(args.app_name))
            with open(os.path.join(dir_name, args.app_name+".py"), "w") as f:
                f.write("""from flask import Flask
app = Flask(__name__)

@app.route('/')
def main():
    return "Working"

if __name__ == '__main__':
    app.run(debug=True)""")
                f.close()
            print("Created {}.py".format(args.app_name))
        elif args.pyramid is True:
            if venv is True:
                print("Creating virtualenv and activating it...")
                command = f"{cd_dir} virtualenv "
                command = command + f"{args.venv_name} && {venv_activate} &&"
                config_dict = {
                    'framework': 'pyramid',
                    'run_command': f'python {args.app_name}.py',
                    'venv_name': args.venv_name,
                    'app_name': args.app_name}
                print("Activated")
            else:
                command = ''
                config_dict = {
                    'framework': 'pyramid',
                    'run_command': f'python {args.app_name}.py',
                    'venv_name': None,
                    'app_name': args.app_name}
            print("Installing pyramid and waitress...")
            subprocess.run(
                f"{command} pip install pyramid waitress", shell=True)
            print("Installed")
            if dir_name == '':
                dir_name = dir_name
            print("Creating {}.py".format(args.app_name))
            with open(os.path.join(dir_name, args.app_name+".py"), "w") as f:
                f.write("""from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response('Working')


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    serve(app,host='127.0.0.1', port=8000)""")
                f.close()
            print("Created {}.py".format(args.app_name))
        print("Creating config files...")
        web_dir = os.path.join(dir_name, ".web")
        os.mkdir(web_dir)
        with open(os.path.join(web_dir, "config.json"), "w") as f:
            json.dump(config_dict, f, indent=4)
            f.close()
        print("Created config files")
        print("Done")

    else:
        print(
            "A project already exists." +
            " Please create a project in another directory" +
            " or delete the project in this directory."
        )


def start() -> None:
    web_dir = os.path.join(".web")
    if os.path.exists(web_dir):
        config_file = os.path.join(web_dir, "config.json")
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                run_command = json.load(f)
                if run_command['venv_name'] is None:
                    command = ''
                elif run_command['venv_name'] is not None:
                    if sys.platform == 'win32':
                        command = os.path.join(
                            run_command['venv_name'], 'Scripts', 'activate'
                        )+" && "
                    else:
                        command = "source ./{args.venv_name}/bin/activate"
                    print("Activating virtualenv {} with {}".format(
                        run_command['venv_name'], command))
                print("Executing {} from config.json in .web directory".format(
                    run_command['run_command']))
                if run_command['framework'] == 'pyramid':
                    print("Running app...")
                subprocess.run(command+run_command['run_command'], shell=True)
    else:
        print(
            "Error: Not a web app project." +
            " Please go into the directory where you have created the project."
        )


def detach() -> None:
    web_dir = os.path.join(".web")
    if os.path.exists(web_dir):
        config_file = os.path.join(web_dir, "config.json")
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                js = json.load(f)
                if js['venv_name'] is None:
                    pass
                else:
                    if js['venv_name'] is not None:
                        if sys.platform == 'win32':
                            command = os.path.join(js['venv_name'], 'Scripts')
                            command = os.path.join(command, 'activate')
                            +" && "
                        else:
                            command = "source ./{args.venv_name}/bin/activate"
                    else:
                        command = ''
                    print("Creating requirements.txt file")
                    subprocess.run(
                        command+"pip freeze > requirements.txt", shell=True)
                    print("Created")
                    f.close()
                if os.path.exists("run.sh") or os.path.join("run.bat"):
                    with open("run_command.sh", "w") as f:
                        f.write('#!/bin/bash\n')
                        f.write(command+js['run_command'])
                        f.close()
                    with open("run_command.bat", "w") as f:
                        f.write(command+js['run_command'])
                        f.close()
                else:
                    with open("run.sh", "w") as f:
                        f.write('#!/bin/bash\n')
                        f.write(command+js['run_command'])
                        f.close()
                    with open("run.bat", "w") as f:
                        f.write(command+js['run_command'])
                        f.close()
                for file in os.listdir(web_dir):
                    os.remove(os.path.join(web_dir, file))
                os.rmdir(web_dir)
                print("Project detached")
    else:
        print(
            "Error: Not a web app project." +
            " Please go into the directory where you have created the project."
        )


def build_parser():
    parser = argparse.ArgumentParser(
        description="Choose the type of service to deploy")
    services = parser.add_mutually_exclusive_group(required=True)
    services.add_argument("-heroku", "--heroku", action='store_true',
                          help="Creates a heroku Procfile", default=False)
    parsed = parser.parse_args()
    if parsed.heroku is True:
        build(heroku=True)


def main():
    parsed_namespace = sys_argv()
    if len(parsed_namespace) > 1:
        if parsed_namespace[1] == ('create' or '--help' or '-h'):
            create_tool(init_argparse(parsed_namespace[1:]))
        elif parsed_namespace[1] == 'run':
            length = len(parsed_namespace[1:])
            if length <= 1 and length >= 0:
                start()
            else:
                print("invalid arguments {}".format(str(parsed_namespace[2:])))
        elif parsed_namespace[1] == 'detach':
            detach()
        elif parsed_namespace[1] == 'build':
            build()
        else:
            init_argparse(parsed_namespace[1:])
    else:
        print("Invalid command. Valid commands are create, run and detach")


def build(heroku: bool = False):
    web_dir = os.path.join(".web")
    if os.path.exists(web_dir):
        config_file = os.path.join(web_dir, "config.json")
        if os.path.exists(config_file):
            f = open(config_file, "r")
            js = json.load(f)
            f.close()
            if js['framework'] == 'fastapi':
                if heroku is True:
                    command = 'uvicorn {}:app --reload'.format(js['app_name'])
                    with open("Procfile", "w") as f:
                        f.write(command)
                        f.close()


if __name__ == '__main__':
    main()
