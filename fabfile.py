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


@hosts('knbase.org@knbase.org')
def collect_static():
    with cd(CODE_DIR):
        run('{0} collectstatic --noinput'.format(PYTHON), pty=True)


@hosts('knbase.org@knbase.org')
def migrate():
    with cd(CODE_DIR):
        run('{0} migrate --all'.format(PYTHON), pty=True)


@hosts('knbase.org@knbase.org')
def restart():
    with cd(HOME_DIR):
        run('./start_project.sh', pty=True)


@hosts('knbase.org@knbase.org')
def deploy():
    git_pull()
    collect_static()
    migrate()
    restart()


