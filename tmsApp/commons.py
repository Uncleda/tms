from .models import *
from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist

def getHostList(queryset):
    '''
    get host ip list from the selected terminals
    '''
    hosts = []
    for instance in queryset:
        hosts.append(instance.ip)
    return hosts

def showUpdatedResult(self, request, rows_updated=0):
    '''
    show action result to user
    '''
    if rows_updated == 0:
        self.message_user(request,
                            "Failed due to some terminals can not be reached!", 
                            level=messages.ERROR)
    else:
        if rows_updated == 1:
            message_bit = "1 terminal was"
        else:
            message_bit = "%s terminals were" % rows_updated
        self.message_user(request,"%s successfully done." % message_bit)

def saveResult2Db(output, result_category='T'):
    '''
    save the fabric execute action result(a dict) to DB
    result_category has three choices: 
    T(Terminal), D(TerminalDevice), S(TerminalSoftware)
    saveResult2Db use the result_category to store data into different models
    '''
    if len(output) < 1:
        pass
        return

    for k, v in output.items():
        try:
	        term = Terminal.objects.get(ip = k)
        except ObjectDoesNotExist:
            term = None
    
        if result_category == 'D':
            for d in v:
                new_device = TerminalDevice()
                for k1, v1 in d.items():
                    setattr(new_device, '{0}'.format(k1), v1)
                term.terminaldevice_set.add(new_device)
                    
        elif result_category == 'S':
            for s in v:
                new_software = TermianalSoftware()
                for k1, v1 in s.items():
                    setattr(new_software, '{0}'.format(k1), v1)
                term.terminalsoftware_set.add(new_software)

        elif result_category == 'T':
            updateFields = []
            for k1, v1 in v.items():
	            setattr(term, '{0}'.format(k1), v1)
	            updateFields.append(k1)

            term.save(update_fields = updateFields)
   
     

