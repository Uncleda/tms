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
def upload_file(src=None, dist=None):
    # hardcode for dist
    #dist = '/tmp'
    with settings(hide('everything')):
        res = put(src, dist, use_sudo = True)
    return res    

@task
@parallel(pool_size = 5)
def install_software(src=None, dist=None, soft_type='TAR', full_name=None):
    # hardcode for dist
    dist = '/tmp'
    with settings(hide('everything')):
        res = upload_file(src, dist)
        if res.succeeded:
            # example for full_name: "tools/nfs-screenshot_0.5.8_i386.tar.gz"
            full_name = full_name.split('/')[1]
            # full_name is "nfs-screenshot_0.5.8_i386.tar.gz"
            pkg = '{0}/{1}'.format(dist, full_name)
            
            if soft_type == 'TAR':
                extension_name = full_name.split('.')[-1]
                
                if extension_name == 'tgz':
                    file_name = full_name.split('.tgz')[0]
                else:
                    file_name = full_name.split('.tar')[0]
                
                if extension_name in ['gz', 'gzip', 'zip', 'tgz']:
                    run('tar -zxvf {0} -C {1}'.format(pkg, dist))
                elif extension_name == 'bz2':
                    run('tar -jxvf {0} -C {1}'.format(pkg, dist))
                print '{0}/{1}'.format(dist, file_name) 
                run('if test -d {0}/{1}; then cd {0}/{1} && ./configure && make && make install && make clean'.format(dist, file_name))
    
            elif soft_type == 'RPM':
                sudo('rpm -ivh {0}'.format(pkg))
            
            elif soft_type == 'DEB':
                sudo('dpkg -i {0}'.format(pkg))

