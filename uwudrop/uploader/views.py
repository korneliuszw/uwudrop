from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import ParseError
from uploader.models import FileUpload, IdentifierDictionary, Uploader, Upload
from uploader.serializers import UploadSerializer

# Create your views here.
def index(request) -> HttpResponse:
    return HttpResponse("Hello world!")

@api_view(['POST'])
def upload(request: Request) -> Response:
    print(request.get_signed_cookie('user_id'))
    if not request.FILES or not request.query_params.get('id'):
        raise ParseError("No file or upload id provided")
    if not has_user_cookie(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    uploader = Uploader(pk=request.get_signed_cookie('user_id'))
    upload = uploader.upload_set.get(pk=request.query_params.get('id'))
    upload.fileupload_set.create(
        file = request.FILES['file']
    )
    return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def begin_upload(request: Request):
    upload_data_serializer = UploadSerializer(data=request.data)
    upload_data_serializer.is_valid(raise_exception=True)
    response = Response(status=status.HTTP_201_CREATED)
    uploader = get_uploader(request) if has_user_cookie(request) else create_uploader(request, response)
    upload = uploader.upload_set.create(**upload_data_serializer.validated_data)
    response.data = UploadSerializer(upload).data
    return response


@api_view(['GET'])
def invalidate_upload(request: Request) -> Response:
    if not has_user_cookie(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    uploader = Uploader(pk=request.get_signed_cookie('user_id'))
    upload = uploader.upload_set.get(identifier=request.query_params.get('id'))
    upload.delete()
    return Response(status=status.HTTP_200_OK)

def has_user_cookie(request: Request) -> bool:
    return request.COOKIES.get('user_id') and request.get_signed_cookie('user_id')

def create_uploader(request: Request, response: Response) -> Uploader:
    ip = request.META.get('REMOTE_ADDR')
    uploader = Uploader(public_ip=ip)
    uploader.save()
    # TODO: Secure cookie
    response.set_signed_cookie("user_id", uploader.pk)
    return uploader

def get_uploader(request: Request) -> Uploader:
    return Uploader.objects.get(pk=request.get_signed_cookie('user_id'))