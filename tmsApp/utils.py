from __future__ import unicode_literals

from django.db import models
from fabric.api import execute
from django.contrib import admin, messages
from .commons import *
from fabfile import *
from .models import *

def getUserName(modeladmin, request, queryset):
    '''
    get the name who is using the terminal 
    and save to DB
    '''
    try:
        output = execute(get_user_name, hosts = getHostList(queryset))
        saveResult2Db(output)
        showUpdatedResult(modeladmin, request, len(output))
    except:
	    showUpdatedResult(modeladmin, request)

getUserName.short_description = "Get User Name"

def getCPUInfo(modeladmin, request, queryset):
    '''
    get CPU info(vendor,cores,speed,cache_size) from terminal
    and save to DB
    '''
    try:
        output = execute(get_cpu_info, hosts = getHostList(queryset))
        saveResult2Db(output)
        showUpdatedResult(modeladmin, request, len(output))
    except:
        showUpdatedResult(modeladmin, request)

getCPUInfo.short_description = "Get CPU Infomation"

def selectResources(modeladmin, request, queryset):
    '''
    select resources to do next action
    '''
    rows_updated = queryset.update(selected = 1)
    showUpdatedResult(modeladmin, request, rows_updated)

selectResources.short_description = "Select Softwares to Install"

def unselectResources(modeladmin, request, queryset):
    rows_updated = queryset.update(selected = 0)
    showUpdatedResult(modeladmin, request, rows_updated)

unselectResources.short_description = "Remove Softwares to Install"

def installSoftware(modeladmin, request, queryset):
    '''
    install the selected software to terminals
    after that unselect software
    '''
    selected_files = Software.objects.filter(selected = 1)
    
    if len(selected_files) == 0:
        modeladmin.message_user(request,
                            "Please select software you want to install first", 
                            level = messages.ERROR)
    else:
        for f in selected_files:
            try:
                output = execute(install_software, hosts = getHostList(queryset), 
                                    src = f.upload.path, soft_type = f.genre, 
                                    full_name = f.upload.name)
                showUpdatedResult(modeladmin, request, len(output))
            except:
                showUpdatedResult(modeladmin, request)

         # No selected software(s) after installing every time
        selected_files.update(selected = 0)

installSoftware.short_description = "Install Software(s)"
