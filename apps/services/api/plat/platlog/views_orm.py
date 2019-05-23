from rest_framework import serializers, viewsets, routers
from rest_framework import permissions, renderers
# from rest_framework.decorators import action
# from rest_framework.response import Response

from services.permissions.plat_permissions import OnlyGetPermittedPermission

from .serializers import PlatOptHistorySerializer
from .models import PlatOptHistory

# ViewSets define the view behavior.
class OPHViewSet(viewsets.ModelViewSet):
    queryset = PlatOptHistory.objects.all()
    serializer_class = PlatOptHistorySerializer

    permission_classes = (permissions.IsAuthenticated, OnlyGetPermittedPermission)

# Routers provide a way of automatically determining the URL conf.
plh_router = routers.DefaultRouter()
plh_router.register(r'plathistory', OPHViewSet)      ### URL的 Debug 测试




