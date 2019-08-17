from django_apscheduler.models import DjangoJob, DjangoJobExecution

from rest_framework import viewsets, routers, serializers


class DjangoJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoJob
        fields = '__all__'


class DjangoJobExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoJobExecution
        fields = '__all__'


class DjangoJobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DjangoJob.objects.all().order_by('-next_run_time')
    serializer_class = DjangoJobSerializer


class DjangoJobExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DjangoJobExecution.objects.all().order_by('-run_time')
    serializer_class = DjangoJobExecutionSerializer


djapscheduler_router = routers.DefaultRouter()
djapscheduler_router.register('dj_jobs', DjangoJobViewSet)
djapscheduler_router.register('dj_jobexs', DjangoJobExecutionViewSet)
