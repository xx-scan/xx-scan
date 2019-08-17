from .models import MailHost, MailAudit

from rest_framework import viewsets, routers, serializers


class MailHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailHost
        fields = '__all__'


class MailAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailAudit
        fields = '__all__'


class MailHostViewSet(viewsets.ModelViewSet):
    queryset = MailHost.objects.all()
    serializer_class = MailHostSerializer


class MailAuditViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MailAudit.objects.all()
    serializer_class = MailAuditSerializer


mail_router = routers.DefaultRouter()
mail_router.register('mail_hosts', MailHostViewSet)
mail_router.register('mail_slogs', MailAuditViewSet)
