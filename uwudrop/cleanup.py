from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django.utils.timezone import make_aware
from datetime import datetime
from datetime import timedelta
from time import sleep
import os

import logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log_expired = logging.getLogger("expired-downloads")
log_stale = logging.getLogger('stalled-uploaders')

PROJECT_NAME="uwudrop"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % PROJECT_NAME)
# Most django imports must happen after settings settings path
import django
django.setup()
from uploader.models import Upload, FileUpload, Uploader
scheduler = BlockingScheduler()

def remove_expired_downloads():
    now = make_aware(datetime.now())
    result = Upload.objects.filter(delete_at__lte=now).delete()
    if result[0] != 0:
        log_expire.info("Deleted %d expired downloads" % result[0])

def remove_stalled_uploaders():
    # Give some time to ensure we don't delete any in progress uploads
    now = make_aware(datetime.now() + timedelta(days=1, hours=5))
    result = Uploader.objects.filter(created_at__lte=now, upload__isnull=True).delete()
    if result[0] != 0:
        log_stale.info("Deleted %d stale uploaders" % result[0])


scheduler.add_job(remove_expired_downloads, 'interval', seconds=5, id='expired_downloads', max_instances=3,coalesce=True)
scheduler.add_job(remove_stalled_uploaders, 'interval', seconds=5, id='stalled_uploaders', max_instances=3,coalesce=True)
scheduler.start()
