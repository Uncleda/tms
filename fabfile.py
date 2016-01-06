from fabric.contrib import django
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *

django.project('tms')

# need to change the following two var in your env
env.user = 'andy'
env.password = 'nji90okm'

env.skip_bad_hosts = True

@task
@parallel(pool_size = 5)
def get_host_name():
    with settings(hide('everything'), warn_only = True):
        name = run('hostname')
        return name

@task
@parallel(pool_size = 5)
def get_cpu_info():
    with settings(hide('everything'), warn_only = True):
        result = {}

	vendor = run('cat /proc/cpuinfo | grep vendor | cut -d":" -f2')
	cores  = run('cat /proc/cpuinfo | grep processor | wc -l')
	speed  = run('cat /proc/cpuinfo | grep MHz | cut -d":" -f2 | head -n 1')
	cache  = run('cat /proc/cpuinfo | grep cache | cut -d":" -f2 | cut -d" " -f2 | head -n 1')
	
	result['vender'] = vender
	result['cores'] = cores
	result['speed'] = speed
	result['cache'] = chche

	return result
	
