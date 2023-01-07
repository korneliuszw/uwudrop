from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('begin', views.begin_upload, name="begin"),
    path('upload', views.upload, name='upload')
]