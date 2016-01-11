from __future__ import unicode_literals

from django.db import models
from fabric.api import *
from django.contrib import admin, messages
from .commons import *
from fabfile import *
from .models import *

def getUserName(modeladmin, request, queryset):
    #host_num = len(queryset)
    try:
        output = execute(get_user_name, hosts = getHostList(queryset))
        saveResult2Db(output)
        showUpdatedResult(modeladmin, request, len(output))
    except:
	    showUpdatedResult(modeladmin, request)

getUserName.short_description = "Get User Name"

def getCPUInfo(modeladmin, request, queryset):
    output = execute(get_cpu_info, hosts = getHostList(queryset))
    saveResult2Db(output)
    showUpdatedResult(modeladmin, request, len(output))
    '''
    for k,v in output.items():
	term = Terminal.objects.get(ip = k)
	print term
	term.cpu_vendor = v.get('cpu_vendor')
	print str(v.get('cpu_vendor'))
	term.cpu_cores = v.get('cpu_cores')
	term.cpu_speed = v.get('cpu_speed')
	term.cache_size = v.get('cache_size')
	term.save()
    '''
getCPUInfo.short_description = "Get CPU Infomation"

def selectResources(modeladmin, request, queryset):
    rows_updated = queryset.update(selected = 1)

selectResources.short_description = "Select Softwares to Install"

def installSoftware(modeladmin, request, queryset):
    selected_files = Software.objects.filter(selected = 1)

    if len(selected_files) == 0:
        pass
    else:
        for f in selected_files:
            try:
                output = execute(install_software, hosts = getHostlist(queryset),
                                    src = f.upload.path, soft_type = f.genre, full_name = f.upload.name)
                showUpdatedResult(modeladmin, request, len(output))
            except:
                showUpdatedResult(modeladmin, request)

         # No selected software(s) after installing every time
        selected_files.update(selected = 0)

installSoftware.short_description = "Install Software(s)"
