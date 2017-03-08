from fabric.api import *
env.use_ssh_config = True
env.hosts = ['dsl']

def deploy():
    code_dir = '~/program/python/flask-lovehate'
    with cd(code_dir):
        run("git pull")
        run("sudo supervisorctl restart lovehate")
