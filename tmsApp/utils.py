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

    try:
        term_info = execute(get_term_info, hosts = host_list)
        showUpdatedResult(modeladmin, request, len(output))

    except:
        showUpdatedResult(modeladmin, request)

    save_changes(term_info)

refresh_term.short_description = "Refresh selected terminals"

def poweron_selected_terms(modeladmin, request, queryset):
    '''
    Power on the remote terminals with the wakeonlan tool
    '''
    try:
        for instance in queryset:
            os.system('wakeonlan ' + instance.mac)
        showUpdatedResult(modeladmin, request, len(queryset))

    except:
        showUpdatedResult(modeladmin, request)

poweron_selected_terms.short_description = "Poweron selected terminals"

def shutdown_selected_terms(modeladmin, request, queryset):
    '''
    Shutdown the remote terminals with "shutdown" command issued.
    '''
    host_list = []
    for instance in queryset:
        host_list.append(instance.ip)

    try:
        result = execute(shutdown_term, hosts = host_list)
        showUpdatedResult(modeladmin, request, len(host_list))

    except:
        showUpdatedResult(modeladmin, request)

    print result

shutdown_selected_terms.short_description = "Shutdown selected terminals"

def reboot_selected_terms(modeladmin, request, queryset):
    '''
    Reboot remote terminals with "reboot" command issued.
    '''
    host_list = []
    for instance in queryset:
        host_list.append(instance.ip)

    try:
        result = execute(reboot_term, hosts = host_list)
        showUpdatedResult(modeladmin, request, len(host_list))

    except:
        showUpdatedResult(modeladmin, request)

    print result

reboot_selected_terms.short_description = "Reboot selected terminals"

def monitor_term(modeladmin, request, queryset, item = 'all'):
    '''
    Redirect to monitor information display page
    '''
    host_list = []
    tags = {}
    for instance in queryset:
        host_list.append(instance.ip)
        tags[instance.ip] = instance.tag

    try:
        monitor_info = execute(get_monitor_info, hosts = host_list)

    except:
        showUpdatedResult(modeladmin, request)

    for ip, result in monitor_info.items():
        monitor_info[ip] = sorted(result.iteritems(), key=lambda asd:asd[0])
        monitor_info[ip][0] = ('1_tag', tags[ip])

    if item == 'all':
        template = "monitor_info.html"
    if item == 'cpu':
        template = "monitor_cpu.html"
        for ip, result in monitor_info.items():
            del monitor_info[ip][3:9]
    if item == 'mem':
        template = "monitor_mem.html"
        for ip, result in monitor_info.items():
            del monitor_info[ip][1:3]
            del monitor_info[ip][4:]
    if item == 'disk':
        template = "monitor_disk.html"
        for ip, result in monitor_info.items():
            del monitor_info[ip][1:6]

    print monitor_info

    context = dict(
        modeladmin.admin_site.each_context(request),
        title="Monitor Information",
        monitor_info=dict(monitor_info).items(),
    )

    request.current_app = modeladmin.admin_site.name

    # Display the monitor page
    return TemplateResponse(request, template, context)
    #return render(request, "admin/monitor_info.html", {'form':form})

monitor_term.short_description = "Display monitor page"

def monitor_cpu(modeladmin, request, queryset):
    '''
    Redirect to monitor cpu page
    '''
    return monitor_term(modeladmin, request, queryset, item = 'cpu')

monitor_cpu.short_description = "Display cpu usage"

def monitor_mem(modeladmin, request, queryset):
    '''
    Redirect to monitor memory page
    '''
    return monitor_term(modeladmin, request, queryset, item = 'mem')

monitor_mem.short_description = "Display memory usage"

def monitor_disk(modeladmin, request, queryset):
    '''
    Redirect to monitor disk page
    '''
    return monitor_term(modeladmin, request, queryset, item = 'disk')

monitor_disk.short_description = "Display disk usage"
