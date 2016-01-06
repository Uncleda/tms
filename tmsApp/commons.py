def getHostList(queryset):
    hosts = []
    for instance in queryset:
        hosts.append(instance.ip)
    return hosts
