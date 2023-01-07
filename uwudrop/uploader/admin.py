from django.contrib import admin
from uploader.models import Upload, Uploader, FileUpload, IdentifierDictionary
# Register your models here.

@admin.register(Uploader)
class UploaderAdmin(admin.ModelAdmin):
    pass
@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    pass
@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    pass
@admin.register(IdentifierDictionary)
class IdentifierDictionaryAdmin(admin.ModelAdmin):
    pass