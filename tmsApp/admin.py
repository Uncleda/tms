from django.contrib import admin

from .models import Terminal, TerminalSoftware, TerminalDevice
from .utils import *

# Register your models here.

class TerminalAdmin(admin.ModelAdmin):
    list_display = ('tag', 'user', 'ip', 'department','project','timestamp','status')
    #fields = (('tag', 'user'), 'ip', 'department','project','mac','cpu_speed')
    fieldsets = (
        ('Basic info',{
            'fields': (('tag','ip'),('user','mac'),'department','project','notes')
        }),
        ('CPU info',{
            'classes':('collapse',),
            'fields':('cpu_vendor','cpu_cores','cpu_speed','cache_size')
        }),
        ('Memory info',{
            'classes':('collapse',),
            'fields':('mem_total','swap_total')
        }),
    )
    search_fields = ['tag','user', 'ip','department','project']
    date_hierarchy = 'timestamp'
    list_display_links = ('tag',)
    readonly_fields = ('cpu_vendor','cpu_cores','cpu_speed','cache_size')
    #list_filter = (('department',admin.filters.DropdownFilter),('project',admin.filters.DropdownFilter),)
    list_filter = ('department','project',)
    list_per_page = 20
    #list_editable

    actions = [getUserName, getCPUInfo]

class TerminalSoftwareAdmin(admin.ModelAdmin):
    list_display = ('id', 'computer', 'software_name','software_version','software_size')
    search_fields = ['software_name','computer']
    list_per_page = 20

class TerminalDeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'computer', 'device_type', 'device_name')
    search_fields = ['device_name','computer']
    list_per_page = 20

admin.site.register(Terminal, TerminalAdmin)
admin.site.register(TerminalSoftware, TerminalSoftwareAdmin)
admin.site.register(TerminalDevice, TerminalDeviceAdmin)
