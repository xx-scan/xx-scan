from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .models import PlatOptHistory


class PlatOptHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatOptHistory
        fields = ('desc', 'type', 'opreatername', 'opreate_time', 'remote_file', 'extra')

