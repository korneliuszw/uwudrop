from django.db import models
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.conf import settings
from random import randint
import logging

logger = logging.getLogger(__name__)
class Uploader(models.Model):
    public_ip = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)


def maxDaysFromNow():
    return make_aware(datetime.now() + timedelta(days=+settings.MAX_FILE_UPLOAD_DAYS))

def generate_identifer():
    word_ids = set()
    if (settings.WORDS < 10):
        logger.critical("set more words!")
    # seed set until exactly 3 elements because every id must be unique
    while len(word_ids) != 3:
        word_ids.add(randint(1, settings.WORDS))
    id = ""
    for x in IdentifierDictionary.objects.filter(pk__in=word_ids):
        id += x.word
    return id
class Upload(models.Model):
    uploader = models.ForeignKey(Uploader, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=50, unique=True, primary_key=True, default=generate_identifer)
    delete_at = models.DateTimeField(default=maxDaysFromNow)
    password = models.CharField(max_length=80, null=True)
    remaining_downloads = models.IntegerField(null=True)

class FileUpload(models.Model):
    file = models.FileField()
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)

class IdentifierDictionary(models.Model):
    word = models.CharField(max_length = 10)
