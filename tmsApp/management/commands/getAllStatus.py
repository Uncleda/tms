from django.core.management.base import BaseCommand, CommandError
from tmsApp.models import Terminal
from tmsApp.commons import *
from fabric.api import *

class Command(BaseCommand):
    help = "Get the status from all terminals"

    def handle(self, *args, **options):
        ip_list = getHostList(Terminal.objects.all())
        for ip in ip_list:
            host = Terminal.objects.get(ip = ip) 
            with settings(hide('everything'), warning = True):
                output = local('ping -c 2 -s 0 {0}'.format(ip), capture = False)
                # if return code is 1, means error while running ping
                host.status = 0 if output.return_code else 1
            host.save()
                
