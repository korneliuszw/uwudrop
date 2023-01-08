from rest_framework import serializers
from uploader.models import maxDaysFromNow, Upload
from django.conf import settings

class UploadSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['delete_at'] > maxDaysFromNow():
            raise serializers.ValidationError(f"Date cannot be greater than {settings.MAX_FILE_UPLOAD_DAYS} days from request time")
        return data
    class Meta:
        model = Upload
        fields = ['delete_at', 'password', 'remaining_downloads', 'identifier']
        read_only_fields = ['identifier']
