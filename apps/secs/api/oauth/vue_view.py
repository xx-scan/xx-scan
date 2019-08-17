# coding:utf-8
import json
from django.http import JsonResponse
from rest_framework.response import Response

# from django.forms.models import model_to_dict
from django.core.paginator import Paginator

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# from .local_config import AccessLogPaginator, ModsecLogPaginator


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def user_info(request):
    return Response(data={
        'username': 'admink'
    })


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def user_logout(request):
    return Response(data={
        'username': 'admink'
    })