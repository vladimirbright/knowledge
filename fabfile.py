# -*- coding: utf-8 -*-

from fabric.api import *
from fabric.contrib.console import confirm


@hosts('knbase@knbase.org')
def deploy():
    with cd('/home/knbase/knowledge'):
        run('git pull', pty=True)

