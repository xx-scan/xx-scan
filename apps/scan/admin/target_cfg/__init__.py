from django.contrib import admin


from ...models import Host, Service

class HostAdmin(admin.ModelAdmin):
    list_display = ("name", "ip", "mac", "mac_vendor", "up")

admin.site.register(Host, HostAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ("host", "port", "banner", "protocol", "service", "version", "descover_time")

admin.site.register(Service, ServiceAdmin)