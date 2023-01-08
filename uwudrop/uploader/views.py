from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import ParseError
from random import randint
from uploader.models import FileUpload, IdentifierDictionary, Uploader
from uploader.serializers import UploadSerializer
import logging
import zipfile

logger = logging.getLogger(__name__)

# Create your views here.
def index(request) -> HttpResponse:
    return HttpResponse("Hello world!")

def upload(request: HttpRequest) -> HttpResponse:
    print(request.get_signed_cookie('user_id'))
    if not request.FILES or not request.get_signed_cookie('user_id'):
        raise ParseError("No file or user_id cookie provided")
    uploader = Uploader.objects.get(pk=request.get_signed_cookie('user_id'))
    uploader.upload_set.create(
        identifier=identifier,
        file = request.FILES
    )

@api_view(['GET'])
def begin_upload(request: Request):
    upload_data_serializer = UploadSerializer(data=request.data)
    upload_data_serializer.is_valid()
    response = Response(status=status.HTTP_201_CREATED)
    uploader = get_uploader(request) if request.get_signed_cookie('user_id') else create_uploader(request, response)

    uploader.upload_set.add(upload_data_serializer)
    # TODO: Figure out whether to save first or after
    upload_data_serializer.save()

    return response

@api_view(['GET'])
def invalidate_upload(request: Request) -> Response:
    upload_data_serializer = UploadSerializer(data=request.data)
    upload_data_serializer.is_valid(raise_exception=True)
    if not request.get_signed_cookie('user_id'):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    upload = Upload(uploader_pk = request.get_signed_cookie('user_id'), identifier=request.query_params.get('id'))
    upload.delete()


def create_uploader(request: Request, response: Response) -> Uploader:
    ip = request.META.get('REMOTE_ADDR')
    uploader = Uploader(public_ip=ip)
    uploader.save()
    # TODO: Secure cookie
    res.set_signed_cookie("user_id", uploader.pk)
    return uploader

def get_uploader(request: Request) -> Uploader:
    return Uploader.objects.get(pk=request.get_signed_cookie('user_id'))

