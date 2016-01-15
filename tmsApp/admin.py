from django.contrib import admin

from .models import Terminal, TerminalSoftware, TerminalDevice, Software, OsImage, File
from .utils import *

# Register your models here.
class TerminalSoftwareInline(admin.TabularInline):
    model = TerminalSoftware
    list_per_page = 5
    max_num = 5
    can_delete = False

class TerminalDeviceInline(admin.TabularInline):
    model = TerminalDevice
    can_delete = False
    max_num = 5

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
    inlines = [TerminalDeviceInline,TerminalSoftwareInline,]
    #list_editable

    actions = [getUserName, getCPUInfo, refresh_term, monitor_term, monitor_cpu, monitor_mem, monitor_disk,
               poweron_selected_terms, shutdown_selected_terms, reboot_selected_terms, installSoftware, installOSimage, 
               transferFiles,launchCommunication]

class TerminalSoftwareAdmin(admin.ModelAdmin):
    list_display = ('id', 'computer', 'software_name','software_version','software_size')
    search_fields = ['software_name','computer']
    list_per_page = 20

class TerminalDeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'computer', 'device_type', 'device_name')
    search_fields = ['device_name','computer']
    list_per_page = 20

class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'genre', 'selected', 'timestamp')
    list_display_links = ('name',)
    search_fields = ['name','genre']
    actions = [selectResources, unselectResources]

class OsImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'genre', 'selected', 'timestamp',)
    list_display_links = ('name',)
    search_fields = ['name', 'genre',]
    actions = [selectResources, unselectResources]

class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'selected', 'timestamp',)
    list_display_links = ('name',)
    search_fields = ['name',]
    actions = [selectResources, unselectResources]

admin.site.register(Terminal, TerminalAdmin)
admin.site.register(TerminalSoftware, TerminalSoftwareAdmin)
admin.site.register(TerminalDevice, TerminalDeviceAdmin)
admin.site.register(Software, SoftwareAdmin)
admin.site.register(OsImage,OsImageAdmin)
admin.site.register(File,FileAdmin)
