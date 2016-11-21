from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^image[/]$', views.get_image, name="image"),
    url(r'^result[/]$', views.view_result, name="result"),
    url(r'^upload[/]$', views.file_upload, name="upload"),
]
