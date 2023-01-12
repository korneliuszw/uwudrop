from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import server_error
from uploader.models import Upload, FileUpload
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
# Create your views here.


@api_view(['GET'])
def downloader(request: Request, pk: str):
    upload = get_object_or_404(Upload, pk=pk)
    if upload.password != None:
        password = request.headers.get('Authorization')
        if not password:
            # Redirect to let user enter the password
            url = settings.FRONTEND_FILE_PASSWORD_URL + pk
            return HttpResponseRedirect(url)
        elif not check_password(password, upload.password):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        file = upload.fileupload
    except FileUpload.DoesNotExist:
        # TODO: Setup upload handler that will remove a stale object if interrupted
        return Response({'error': "Upload failed during the upload process."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    response = HttpResponse(file.file, 'text/plain')
    response['Content-Disposition'] = f"attachment; filename={file.originalFileName}"
    if upload.remaining_downloads != None:
        upload.remaining_downloads = upload.remaining_downloads - 1
        if upload.remaining_downloads > 0:
            upload.save()
        else:
            upload.delete()
    return response
        