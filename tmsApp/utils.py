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
getCPUInfo.short_description = "Get CPU infomation"

def launchCommunication(modeladmin,request,queryset):
    #output = execute(launch_communication,hosts = getHostList(queryset))
    #TODO save the result to the specific data structure to show in the net page
    #print output
    for item in getHostList(queryset):
        output = execute(launch_communication, host = item)

launchCommunication.short_description = "Launch Communication"

