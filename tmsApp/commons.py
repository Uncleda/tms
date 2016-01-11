from .models import *
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

def getHostList(queryset):
    hosts = []
    for instance in queryset:
        hosts.append(instance.ip)
    return hosts

def showUpdatedResult(self, request, rows_updated=0):
    if rows_updated == 0:
        self.message_user(request,"Failed due to some terminals can not be reached!", level=messages.ERROR)
    else:
        if rows_updated == 1:
            message_bit = "1 terminal was"
        else:
            message_bit = "%s terminals were" % rows_updated
        self.message_user(request,"%s successfully done." % message_bit)

def saveResult2Db(output):
    if len(output) >= 1:
	    for k, v in output.items():
	        try:
		        term = Terminal.objects.get(ip = k)
		        updateFields = []
	        except ObjectDoesNotExist:
		        term = None
	
	        for k1, v1 in v.items():
	            setattr(term, '{0}'.format(k1), v1)
	            updateFields.append(k1)

	    term.save(update_fields = updateFields)
    else:
        pass

