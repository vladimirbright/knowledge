# -*- coding: utf-8 -*-


from fabric.api import cd, run, hosts


@hosts('knbase.org@knbase.org')
def gp():
    with cd('/home/knbase.org/www'):
        run('git pull', pty=True)

