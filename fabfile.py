from fabric.api import *
env.use_ssh_config = True
env.hosts = ['dsl']


def deploy():
    code_dir = '~/program/python/flask-lovehate'
    with cd(code_dir):
        run("git pull")
        run("~/.pyenv/versions/lovehate/bin/pip install -r requirements.txt")
        run("~/.pyenv/versions/lovehate/bin/python manage.py db upgrade")
        run("sudo supervisorctl restart lovehate")
