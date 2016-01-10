import string
from fabric.contrib import django
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *

django.project('tms')

# need to change the following two var in your env
env.user = 'oem'
env.password = '123456'

env.warn_only = True
env.skip_bad_hosts = True
env.timeout = 3
env.preconnect = True

@task
@parallel(pool_size = 5)
def get_user_name():
    with settings(hide('warnings')):
	result = {}
        
	result['user'] = run('who | head -n 1 | cut -d" " -f1')
        
	return result

@task
@parallel(pool_size = 5)
def get_cpu_info():
    with settings(hide('everything'), warn_only = True):
        result = {}

	result['cpu_vendor'] = str(run('cat /proc/cpuinfo | grep vendor | cut -d":" -f2 | head -n 1'))
	result['cpu_cores']  = int(run('cat /proc/cpuinfo | grep processor | wc -l'))
	result['cpu_speed']  = float(run('cat /proc/cpuinfo | grep MHz | cut -d":" -f2 | head -n 1'))
	result['cache_size']  = float(run('cat /proc/cpuinfo | grep cache | cut -d":" -f2 | cut -d" " -f2 | head -n 1'))
	print type(result['cpu_vendor']), result['cpu_vendor']

	return result
	
@task
@parallel(pool_size = 5)
def get_term_info():
    with settings(hide('everything'), warn_only = True):
        result = {}
        result['tag'] = run('hostname')
        result['user'] = run('who | head -n 1 | cut -d" " -f1')
        result['mac'] = run("ifconfig | grep HWaddr | awk '{print $NF}'")
        result['cpu_vendor'] = str(run('cat /proc/cpuinfo | grep vendor | cut -d":" -f2 | head -n 1'))
        result['cpu_cores']  = int(run('cat /proc/cpuinfo | grep processor | wc -l'))
        result['cpu_speed']  = float(run('cat /proc/cpuinfo | grep MHz | cut -d":" -f2 | head -n 1'))
        result['cache_size']  = float(run('cat /proc/cpuinfo | grep cache | cut -d":" -f2 | cut -d" " -f2 | head -n 1'))

        return result

@task
@parallel(pool_size = 5)
def get_monitor_info():
    with settings(hide('everything'), warn_only = True):
        #cpu_user = string.atof(run("cat /proc/stat | grep '^cpu ' | cut -d' ' -f3"))
        #cpu_sys = string.atof(run("cat /proc/stat | grep '^cpu ' | cut -d' ' -f4"))
        #cpu_nice = string.atof(run("cat /proc/stat | grep '^cpu ' | cut -d' ' -f5"))
        #cpu_idle = string.atof(run("cat /proc/stat | grep '^cpu ' | cut -d' ' -f6"))
        #cpu_percent = (cpu_user + cpu_sys + cpu_nice) / (cpu_user + cpu_sys + cpu_nice + cpu_idle) * 100

        cpu_percent = 100 - string.atof(run("top -n 1 -b | grep -i '^%Cpu' | awk -F ',' '{print $4}' | sed 's/^[ \t]*//g' | cut -d' ' -f1"))

        memory_total = run("free | grep Mem | sed 's/ \+/ /g' | cut -d' ' -f2")
        memory_used = run("free | grep Mem | sed 's/ \+/ /g' | cut -d' ' -f3")

        disk_percent = run("df -h | grep ' \/$' | sed 's/ \+/ /g' | cut -d' ' -f5")

        result = {}
        result['cpu_percent'] = str("%.2f" % cpu_percent) + "%"
        result['memory_percent'] = str("%.2f" % (string.atof(memory_used) / string.atof(memory_total) * 100)) + "%"
        result['disk_percent'] = disk_percent

        return result

@task
@parallel(pool_size = 5)
def poweron_term():
    with settings(hide('everything'), warn_only = True):

        result = {}
        result['ret'] = run("shutdown -h now")

        return result

@task
@parallel(pool_size = 5)
def shutdown_term():
    with settings(hide('everything'), warn_only = True):

        result = {}
        result['ret'] = run("shutdown -h now")

        return result

@task
@parallel(pool_size = 5)
def reboot_term():
    with settings(hide('everything'), warn_only = True):

        result = {}
        result['ret'] = run("reboot")

        return result

