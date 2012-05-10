# -*- coding: utf-8 -*-


from fabric.api import cd, run, hosts

HOME_DIR = '/home/knbase.org'
CODE_DIR = '/home/knbase.org/www'
ENV_DIR = '/home/knbase.org/Env'

PYTHON = u'%s/bin/python %s/manage.py ' %(ENV_DIR, CODE_DIR)


@hosts('knbase.org@knbase.org')
def git_pull():
    with cd(CODE_DIR):
        run('git pull', pty=True)

