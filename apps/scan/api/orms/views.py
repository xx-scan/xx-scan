from rest_framework import serializers, viewsets, routers
# from rest_framework import permissions, renderers
# from rest_framework.decorators import action
# from rest_framework.response import Response

from .serializers import ScanTool, ScanRecode, Scheme, Host, Service, \
    Protocol, NmapServiceName, ScanReport, ScanTask, ReportFormat

from .serializers import ScanToolSerializer, ScanRecodeSerializer, SchemeSerializer, HostSerializer, ServiceSerializer, \
    ProtocolSerializer, NmapServiceNameSerializer, ScanReportSerializer, ScanTaskSerializer, ReportFormatSerializer


class ScanToolViewSet(viewsets.ModelViewSet):
    queryset = ScanTool.objects.all()
    serializer_class = ScanToolSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class ScanRecodeViewSet(viewsets.ModelViewSet):
    queryset = ScanRecode.objects.all()
    serializer_class = ScanRecodeSerializer


class SchemeViewSet(viewsets.ModelViewSet):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ProtocolViewSet(viewsets.ModelViewSet):
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer


class NmapServiceNameViewSet(viewsets.ModelViewSet):
    queryset = NmapServiceName.objects.all()
    serializer_class = NmapServiceNameSerializer


class ScanReportViewSet(viewsets.ModelViewSet):
    queryset = ScanReport.objects.all()
    serializer_class = ScanReportSerializer


class ScanTaskViewSet(viewsets.ModelViewSet):
    queryset = ScanTask.objects.all()
    serializer_class = ScanTaskSerializer


class ReportFormatViewSet(viewsets.ModelViewSet):
    queryset = ReportFormat.objects.all()
    serializer_class = ReportFormatSerializer


scan_v1_router = routers.DefaultRouter()
scan_v1_router.register(r'hosts', HostViewSet)
scan_v1_router.register(r'services', ServiceViewSet)

scan_v1_router.register(r'protocal', ProtocolViewSet)
scan_v1_router.register(r'nmap_service_names', NmapServiceNameViewSet)

scan_v1_router.register(r'scan_tools', ScanToolViewSet)
scan_v1_router.register(r'scan_recodes', ScanRecodeViewSet)
scan_v1_router.register(r'scan_reports', ScanReportViewSet)
scan_v1_router.register(r'scan_tasks', ScanTaskViewSet)
scan_v1_router.register(r'scan_schemes', SchemeViewSet)
scan_v1_router.register(r'report_formats', ReportFormatViewSet)



