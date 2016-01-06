from __future__ import unicode_literals

from django.db import models
from fabric.api import *
from django.contrib import admin
from fabfile import *

# Create your models here.

class Terminal(models.Model):
    id = models.AutoField('ID', primary_key = True)
    status = models.BooleanField(default = False, editable = False)
    tag = models.CharField(max_length = 30)
    user = models.CharField(max_length = 30, blank = True)
    ip = models.GenericIPAddressField(u'IP')
    timestamp = models.DateTimeField(u'updatetime',auto_now=True, blank = True)
    mac = models.CharField(max_length = 48, blank = True)
    department = models.CharField(max_length = 20, blank = True)
    project = models.CharField(max_length = 20, blank = True)
    notes = models.TextField(blank = True)

    cpu_vendor = models.CharField(max_length = 20, blank = True)
    cpu_cores = models.PositiveIntegerField(u'CPU Cores', default = 1)
    cpu_speed = models.FloatField(u'CPU Speed(MHz)', default = 0)
    cache_size = models.FloatField(u'Cache Size(KB)', default = 0)

    mem_total = models.PositiveIntegerField(u'Memory Total(KB)', default = 0)
    swap_total = models.PositiveIntegerField(u'Swap Total(KB)', default = 0)

    def __unicode__(self):
        return self.tag

class TerminalSoftware(models.Model):
    computer = models.ForeignKey(Terminal)
    software_name = models.CharField(u'Name', max_length = 40, blank = True)
    software_version = models.CharField(u'Version', max_length = 20, blank = True)
    software_size = models.FloatField(u'Size', default = 0)

    def __unicode__(self):
        return self.software_name

class TerminalDevice(models.Model):
    DEVICE_TYPE_CHOISES = (
        ('I', 'Input Device'),
        ('O', 'Monitor Device'),
        ('P', 'Printer Device'),
        ('U', 'USB Device'),
    )
    computer = models.ForeignKey(Terminal)
    device_type = models.CharField(max_length = 20,
                                    choices = DEVICE_TYPE_CHOISES,
                                    null = True)
    device_name = models.CharField(max_length = 40, blank = True)

    def __unicode__(self):
        return self.device_name


