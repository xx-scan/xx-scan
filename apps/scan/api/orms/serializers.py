from rest_framework import serializers
from ...models import ScanTool, ScanRecode, Scheme, Host, Service, \
    Protocol, NmapServiceName, ScanReport, ScanTask, ReportFormat, ScanScript

class ScanToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanTool
        fields = '__all__'
        # fields = ('rule_id', 'phaser', 'param', 'maxlength', 'is_active')
        # fields = ('rule_id', 'phaser', 'param', 'maxlength', 'is_active', )

class ScanScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanScript
        fields = '__all__'
        # fields = ('rule_id', 'phaser', 'param', 'maxlength', 'is_active')
        # fields = ('rule_id', 'phaser', 'param', 'maxlength', 'is_active', )

class ScanRecodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanRecode
        fields = '__all__'
        # fields = ('rule_id', 'phaser', 'param', 'maxlength', 'is_active')

class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = '__all__'
        # fields = ('rule_id', 'phaser', 'param', 'maxlength', 'is_active')

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = '__all__'

class NmapServiceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = NmapServiceName
        fields = '__all__'

class ScanReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanReport
        fields = '__all__'

class ScanTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanTask
        fields = '__all__'

class ReportFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFormat
        fields = '__all__'


from ...models import ServicePort
class ServicePortSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePort
        fields = '__all__'