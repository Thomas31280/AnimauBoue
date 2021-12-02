from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),               # On appel la vue index de l'app administration avec ce schéma d'url
    url(r'^connect_admin_space', views.connect_admin_space, name = "connect_admin_space"),
    url(r'^update_profile_interface', views.update_profile_interface, name = "update_profile"),
    url(r'^administration_interface', views.administration_interface, name = "administration_interface"),
    url(r'^parks_availability', views.consult_parks_availability, name = "consult_parks_availability"),
    url(r'^clients_profiles', views.clients_profiles, name = "clients_profiles"),
]
