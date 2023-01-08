from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@api_view(['GET'])
@csrf_exempt
def csrf(request: Request) -> Response:
    return Response(data={
        'csrfToken': get_token(request)
    })
