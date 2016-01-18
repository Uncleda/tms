# -*- coding: utf-8 -*-
from fabric.contrib import django
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
import string

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
def get_terminal_devices():
    with settings(hide('everything'), warn_only = True):
        result = []
	    # The input USB device
        input_usb_num = int(run('cat /proc/bus/input/devices | grep Bus=0003 | wc -l'))
        if input_usb_num:
            for iter in range(input_usb_num):
                per_result = {}
                per_result['device_type'] = 'I'
                per_result['device_name'] = run("""sed -n '/Bus=0003/N;s/.*\\n\(.*\)/\\1/p' /proc/bus/input/devices | sed 's/\(.*\)"\(.*\)"\(.*\)/\\2/g' | sed -n '{0}p'""".format(iter + 1))
                result.append(per_result)
        # The USB device
        usb_num = int(run("lsusb | sed '/root hub/d' | sed '/Mouse/d' | sed '/Keyboard/d' | wc -l"))
        if usb_num:
            for iter in range(usb_num):
                per_result = {}
                per_result['device_type'] = 'U'
                per_result['device_name'] = run("lsusb | sed '/root hub/d' | sed '/Mouse/d' | sed '/Keyboard/d' | cut -d' ' -f7- | sed -n '{0}p'".format(iter + 1))
                result.append(per_result)
        # The monitor model type
	    with cd('/sys/class/drm'):
	        monitor_card_path = run('''find card*/enabled -type f | xargs grep "enabled" | cut -d'/' -f1''')
            if monitor_card_path[:4] == 'card':
                monitor_result = {}
                monitor_result['device_type'] = 'O'
                monitor_result['device_name'] = run("cat {0}/edid | edid-decode | grep 'Monitor name' | cut -d':' -f2 | cut -b 2-".format(monitor_card_path))
                result.append(monitor_result)
    return result
	
@task
@parallel(pool_size = 5)
def get_terminal_softwares():
    with settings(hide('everything'), warn_only = True):
        result = []
        with cd('/usr/share/nfs/help/html/software'):
            result_num = int(run('''find *.html -type f | xargs sed -n '/<span class ="tw"><a href=/p' | wc -l'''))
	    if result_num:
                for iter in range(result_num):
                    per_result = {}
                    per_result['software_name'] = run("""find *.html -type f | xargs sed -n '/<span class ="tw"><a href=/p' | sed 's/^[<p>]*//g' | cut -d'>' -f3 | cut -d' ' -f2 | sed 's/[</a]*$//g' | sed -n '{0}p'""".format(iter + 1))
                    per_result['software_version'] = ''
                    per_result['soltware_size'] = ''
                    result.append(per_result)
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

@task
@parallel(pool_size = 5)
def install_OSimage(src=None, dist=None, soft_type='ISO', full_name=None):
    # hardcode for dist
    dist = "/tmp"
    sudo('if [ ! -d {0} ];then mkdir -p {0};fi'.format(dist))
    with settings(hide('everything')):
        res = upload_file(src, dist)
        if res.succeeded:
            if soft_type == 'ISO':
                full_name = '{0}/{1}'.format(dist, full_name.split('/')[1])
                # 1. Mount iso image
                mount_path = '/mnt/cdrom'
                sudo('if [ ! -d {0} ];then mkdir -p {0};fi'.format(mount_path))
                sudo('mount -o loop -t iso9660 {0} {1}'.format(full_name,mount_path))
                # 2. Get the kernal boot file and copy it to the 'dist' dir 
                vmlinuz_path = run('find {0} -name vmlinuz*'.format(mount_path))
                initrd_path = run('find {0} -name initrd*'.format(mount_path))
                sudo('cp {0} {1}'.format(vmlinuz_path,dist))
                sudo('cp {0} {1}'.format(initrd_path,dist))
                # 3. Modify the grub configuration
                vmlinuz_path = '{0}/{1}'.format(dist,vmlinuz_path.split('/')[-1])
                initrd_path = '{0}/{1}'.format(dist,initrd_path.split('/')[-1])
                local('touch tmsApp/static/admin/conf/grub.cfg')
                with open('tmsApp/static/admin/conf/template_grub.cfg','r') as f:
                    lines = f.readlines()
                with open('tmsApp/static/admin/conf/grub.cfg','w') as f:
                    for line in lines:
                        f.write(line.replace('$vmlinuz_path',vmlinuz_path)
				.replace('$initrd_path',initrd_path)
				.replace('$isoImage_path',full_name))
                # 4. upload the grub configuration to the host and reboot
                upload_file('tmsApp/static/admin/conf/grub.cfg','/boot/grub')
                local('rm -rf tmsApp/static/admin/conf/grub.cfg')
                sudo('umount {0}'.format(mount_path))
                sudo('reboot')
            elif soft_type == 'IMG':
                #TBD in the future
                pass

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

        memory_total = run("free -m| grep Mem | sed 's/ \+/ /g' | cut -d' ' -f2")
        memory_used = run("free -m| grep Mem | sed 's/ \+/ /g' | cut -d' ' -f3")

        disk_total = run("df -m | grep ' \/$' | sed 's/ \+/ /g' | cut -d' ' -f2")
        disk_used = run("df -m | grep ' \/$' | sed 's/ \+/ /g' | cut -d' ' -f3")
        disk_percent = run("df -m | grep ' \/$' | sed 's/ \+/ /g' | cut -d' ' -f5")

        process_count = run("ps -ef | wc -l")

        result = {}
        result['1_tag'] = "Tag"
        result['2_process_count'] = str("%d" % (string.atoi(process_count) - 3))
        result['3_cpu_percent'] = str("%.2f" % cpu_percent) + "%"
        result['4_memory_used'] = str("%.1f" % (string.atof(memory_used) / 1024)) + "G"
        result['5_memory_total'] = str("%.1f" % (string.atof(memory_total) / 1024)) + "G"
        result['6_memory_percent'] = str("%.2f" % (string.atof(memory_used) / string.atof(memory_total) * 100)) + "%"
        result['7_disk_used'] = str("%.1f" % (string.atof(disk_used) / 1024)) + "G"
        result['8_disk_total'] = str("%.1f" % (string.atof(disk_total) / 1024)) + "G"
        result['9_disk_percent'] = disk_percent

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
        #result['ret'] = run("reboot")
        result['ret'] = reboot(wait = 30)

        return result
