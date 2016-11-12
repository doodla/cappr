from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^cappr/image/$', views.cappr_image, name="image"),
    url(r'^cappr/$', views.cappr_redirect),
    url(r'^cappr/view/$', views.cappr_view, name="view"),
    url(r'^add[/]$', views.add_caps, name="add_caps"),
]