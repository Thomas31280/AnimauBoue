from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),               # On appel la vue index de l'app administration avec ce schéma d'url
    url(r'^connect_admin_space', views.connect_admin_space, name = "connect_admin_space"),
    url(r'^logout', views.user_logout, name = "logout"),
    url(r'^update_profile_interface', views.update_profile_interface, name = "update_profile"),
    url(r'^administration_interface', views.administration_interface, name = "administration_interface"),
    url(r'^parks_availability', views.parks_availability, name = "consult_parks_availability"),
    url(r'^clients_profiles', views.clients_profiles, name = "clients_profiles"),
    url(r'^client/$', views.client, name = "client"),
    url(r'^update_client/$', views.update_client, name = "update_client"),
    url(r'^delete_client/$', views.delete_client, name = "delete_client"),
    url(r'^add_client_form', views.add_client_form, name = "add_client_form"),
    url(r'^reservation_form', views.reservation_form, name = "reservation_form"),
    url(r'^arrival-departure_interface', views.arrival_and_departure_interface, name = "arrival-departure_interface"),
    url(r'^add_dog/$', views.add_dog, name = "add_dog"),
    url(r'^delete_dog/$', views.delete_dog, name = "delete_dog"),
    url(r'^add_reservation/$', views.add_reservation, name = "add_reservation"),
]
