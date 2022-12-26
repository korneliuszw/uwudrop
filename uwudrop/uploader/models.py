from django.db import models

class Uploader(models.Model):
    public_ip = models.CharField(max_length=40)
    cookie = models.TextField()

class File(models.Model):
    upload_path = models.TextField()
    uploader = models.ForeignKey(Uploader, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=50, unique=True, primary_key=True)
    delete_at = models.DateTimeField()
    remaining_downloads = models.IntegerField(null=True)
