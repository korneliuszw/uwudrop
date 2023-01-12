from rest_framework.urlpatterns import format_suffix_patterns
from downloader.views import downloader
from django.urls import path
urlpatterns = [
    path('<str:pk>', downloader)
]