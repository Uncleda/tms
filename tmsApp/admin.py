from collections import OrderedDict
from django.contrib import admin
from django.db.models.fields import BLANK_CHOICE_DASH
from django.contrib.admin.utils import model_format_dict
from django.contrib.admin import helpers
from django.utils import six

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
    def __init__(self, *args, **kwargs):
        super(TerminalAdmin, self).__init__(*args, **kwargs)
        self.action_form_list = None

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

    actions = [getUserName, getCPUInfo, refresh_term, poweron_selected_terms, shutdown_selected_terms, reboot_selected_terms,
               installSoftware, installOSimage, transferFiles, monitor_term, monitor_cpu, monitor_mem, monitor_disk]

    general_actions = [getUserName, getCPUInfo, refresh_term]
    control_actions = [poweron_selected_terms, shutdown_selected_terms, reboot_selected_terms]
    install_actions = [installSoftware, installOSimage, transferFiles]
    monitor_actions = [monitor_term, monitor_cpu, monitor_mem, monitor_disk]
    message_actions = [monitor_term]

    def get_actions_in_list(self, request, act_type):

        actions = []

        class_actions = getattr(self.__class__, act_type, [])

        actions.extend(self.get_action(action) for action in class_actions)

        # get_action might have returned None, so filter any of those out.
        actions = filter(None, actions)

        # Convert the actions into an OrderedDict keyed by name.
        actions = OrderedDict(
            (name, (func, name, desc))
            for func, name, desc in actions
        )

        return actions

    def get_action_choices_in_list(self, request, act_type="control_actions"):
        """
        Return a list of choices for use in a form object.  Each choice is a
        tuple (name, description).
        """
        choices = [] + BLANK_CHOICE_DASH
        for func, name, description in six.itervalues(self.get_actions_in_list(request, act_type)):
            choice = (name, description % model_format_dict(self.opts))
            choices.append(choice)
        return choices

    def changelist_view(self, request, extra_context=None):

        self.general_action_form = self.action_form(auto_id=None)
        self.general_action_form.fields['action'].choices = self.get_action_choices_in_list(request, "general_actions")

        self.control_action_form = self.action_form(auto_id=None)
        self.control_action_form.fields['action'].choices = self.get_action_choices_in_list(request, "control_actions")

        self.install_action_form = self.action_form(auto_id=None)
        self.install_action_form.fields['action'].choices = self.get_action_choices_in_list(request, "install_actions")

        self.monitor_action_form = self.action_form(auto_id=None)
        self.monitor_action_form.fields['action'].choices = self.get_action_choices_in_list(request, "monitor_actions")

        self.message_action_form = self.action_form(auto_id=None)
        self.message_action_form.fields['action'].choices = self.get_action_choices_in_list(request, "message_actions")

        return super(TerminalAdmin, self).changelist_view(request, extra_context)



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
