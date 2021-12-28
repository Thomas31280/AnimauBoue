from django.conf.urls import url

from . import views
from user.views import ConsultAvailability

urlpatterns = [
    url(r'^consult_availability', ConsultAvailability.as_view(), name = "consult_availability"),
]
