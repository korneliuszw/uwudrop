from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
class Uploader(models.Model):
    public_ip = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)


def maxDaysFromNow():
    return datetime.now() + timedelta(days=+settings.MAX_FILE_UPLOAD_DAYS)
class Upload(models.Model):
    uploader = models.ForeignKey(Uploader, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=50, unique=True, primary_key=True)
    delete_at = models.DateTimeField(default=maxDaysFromNow())
    password = models.CharField(max_length=80, null=True)
    remaining_downloads = models.IntegerField(null=True)

class FileUpload(models.Model):
    file = models.FileField()
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)

class IdentifierDictionary(models.Model):
    word = models.CharField(max_length = 10)
