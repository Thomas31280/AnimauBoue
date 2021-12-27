from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from administration.views import connect_admin_space, update_profile, parks_availability, add_client_form, reservation_form, add_reservation, arrival_and_departure, update_client, add_dog, update_reservation, update_dog, stats

urlpatterns = [
    url(r'^$', views.index, name = "index"),               # On appel la vue index de l'app administration avec ce schéma d'url
    url(r'^connect_admin_space', connect_admin_space.as_view(), name = "connect_admin_space"),
    url(r'^logout', views.user_logout, name = "logout"),
    url(r'^update_profile', login_required(update_profile.as_view()), name = "update_profile"),
    url(r'^administration_interface', views.administration_interface, name = "administration_interface"),
    url(r'^parks_availability', parks_availability.as_view(), name = "parks_availability"),
    url(r'^clients_profiles', views.clients_profiles, name = "clients_profiles"),
    url(r'^client/$', views.client, name = "client"),
    url(r'^update_client/$', update_client.as_view(), name = "update_client"),
    url(r'^delete_client/$', views.delete_client, name = "delete_client"),
    url(r'^add_client_form', add_client_form.as_view(), name = "add_client_form"),
    url(r'^reservation_form', reservation_form.as_view(), name = "reservation_form"),
    url(r'^arrival-departure_interface', arrival_and_departure.as_view(), name = "arrival-departure_interface"),
    url(r'^add_dog/$', add_dog.as_view(), name = "add_dog"),
    url(r'^delete_dog/$', views.delete_dog, name = "delete_dog"),
    url(r'^add_reservation/$', add_reservation.as_view(), name = "add_reservation"),
    url(r'^client_reservations/$', views.client_reservations, name = "client_reservations"),
    url(r'^delete_reservation', views.delete_reservation, name = "delete_reservation"),
    url(r'^update_reservation', update_reservation.as_view(), name = "update_reservation"),
    url(r'^update_dog', update_dog.as_view(), name = "update_dog"),
    url(r'^stats', stats.as_view(), name = "stats"),
]
