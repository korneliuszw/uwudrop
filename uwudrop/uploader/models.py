from django.db import models

class Uploader(models.Model):
    public_ip = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

class Upload(models.Model):
    uploader = models.ForeignKey(Uploader, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=50, unique=True, primary_key=True)
    delete_at = models.DateTimeField(null=True)
    remaining_downloads = models.IntegerField(null=True)

class FileUpload(models.Model):
    file = models.FileField()
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)

class IdentifierDictionary(models.Model):
    word = models.CharField(max_length = 10)
