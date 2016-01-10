from __future__ import unicode_literals

from django.db import models
from fabric.api import *
from django.contrib import admin, messages
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from .commons import *
from fabfile import *
from .models import *
import os

def save_changes(new_changes):
    '''
    save the updates to database
    '''
    for ip_addr, result in new_changes.items():
        updateFields = []
        term = Terminal.objects.get(ip = ip_addr)

        for key, value in result.items():
            setattr(term, '{0}'.format(key), value)
            updateFields.append(key)

        term.save(update_fields = updateFields)

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

def refresh_term(modeladmin, request, queryset):
    '''
    Query information from remote termainals and 
    refresh the database with the receivced data.
    '''
    host_list = []
    for instance in queryset:
        host_list.append(instance.ip)

    term_info = execute(get_term_info, hosts = host_list)

    save_changes(term_info)

refresh_term.short_description = "Refresh selected terminals"

def poweron_selected_terms(modeladmin, request, queryset):
    '''
    Power on the remote terminals with the wakeonlan tool
    '''
    for instance in queryset:
        os.system('/usr/bin/wakeonlan ' + instance.mac)

poweron_selected_terms.short_description = "Poweron selected terminals"

def shutdown_selected_terms(modeladmin, request, queryset):
    '''
    Shutdown the remote terminals with "shutdown" command issued.
    '''
    host_list = []
    for instance in queryset:
        host_list.append(instance.ip)

    result = execute(shutdown_term, hosts = host_list)

    print result

shutdown_selected_terms.short_description = "Shutdown selected terminals"

def reboot_selected_terms(modeladmin, request, queryset):
    '''
    Reboot remote terminals with "reboot" command issued.
    '''
    host_list = []
    for instance in queryset:
        host_list.append(instance.ip)

    result = execute(reboot_term, hosts = host_list)

    print result

reboot_selected_terms.short_description = "Reboot selected terminals"

def monitor_term(modeladmin, request, queryset):
    '''
    Redirect to monitor information display page
    '''
    host_list = []
    for instance in queryset:
        host_list.append(instance.ip)

    monitor_info = execute(get_monitor_info, hosts = host_list)

    print monitor_info

    context = dict(
        modeladmin.admin_site.each_context(request),
        title=_("Monitor Information"),
        monitor_info=dict(monitor_info).items(),
    )

    request.current_app = modeladmin.admin_site.name

    # Display the monitor page
    return TemplateResponse(request, "monitor_info.html", context)
    #return render(request, "admin/monitor_info.html", {'form':form})

monitor_term.short_description = "Display monitor page"

