from django.contrib import admin


from .models import ScanTool, ScanRecode, Scheme, Host, Service, \
    Protocol, NmapServiceName, ScanReport, ScanTask, ReportFormat


for Model in (ScanTool, ScanRecode, Scheme, Host, Service, \
    Protocol, NmapServiceName, ScanReport, ScanTask, ReportFormat):
    admin.site.register(Model)

