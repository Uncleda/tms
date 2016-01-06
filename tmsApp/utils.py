from __future__ import unicode_literals

from django.db import models
from fabric.api import *
from django.contrib import admin
from .commons import *

def getHostName(modeladmin, request, queryset):
    #host_num = len(queryset)
    output = execute(get_host_name, hosts = getHostlist(queryset))
    # output is a dictionary
    # which like {u'192.168.233.138': 'dev1', u'192.168.233.139': 'dev2'}
    #for k,v in output.items():
    #    res[k] = str(v)
    #    print k, str(v)
    
    # TODO save the result to db

   #rows_updated = queryset.update(status = 1)
   #     if rows_updated == 1:
   #         message_bit = "1 computer was"
   #     else:
   #         message_bit = "%s computers were" % rows_updated

   #    self.message_user(request,"%s successfully done." % message_bit)

getHostName.short_description = "Get Host Name"

def getCPUInfo(modeladmin, request, queryset):
    output = execute(get_cpu_info, hosts = getHostlist(queryset))
    # TODO save the result to db

getCPUInfo.short_description = "Get CPU infomation"
