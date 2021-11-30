from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),               # On appel la vue index de l'app administration avec ce schéma d'url
]