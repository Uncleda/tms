from .models import *
from django.contrib import admin

def getHostList(queryset):
    hosts = []
    for instance in queryset:
        hosts.append(instance.ip)
    return hosts

def saveResult2Db(output):
    for k, v in output.items():
	term = Terminal.objects.get(ip = k)
	updateFields = []
	
	for k1, v1 in v.items():
	    setattr(term, '{0}'.format(k1), v1)
	    updateFields.append(k1)

	term.save(update_fields = updateFields)

