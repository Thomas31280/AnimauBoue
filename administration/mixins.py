from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from .forms import SelectTimeFrameForm
import datetime
import calendar
from django.utils.timezone import make_aware
from administration.models import Reservations


class SuperUserRequired(UserPassesTestMixin):
    def super_user(self):
        return self.request.user.is_superuser


class PlanningNStats(View, SuperUserRequired):
    form_class = SelectTimeFrameForm

    def reservations_in_interval(self, time_frame, build_array):
        year = int(time_frame.cleaned_data['year'])
        month = int(time_frame.cleaned_data['month'])
        num_days = calendar.monthrange(year, month)[1]

        # On détermine le premier et dernier jour du mois, en utilisant le module datetime pour créer un objet de type datetime, et en utilisant sur cet objet la méthode django make_aware, qui permet de donner à l'objet datetime un attribut .tzinfo, qui contient des informations sur la timezone. Sans cela, il serait impossible de faire une compraison avec les datetimes présents en base de données
        first_day = make_aware(datetime.datetime(year, month, 1))
        last_day = make_aware(datetime.datetime(year, month, num_days, 23, 59, 59))

        # Dans la base de données, on va aller chercher tous les éléments :
        # - Dont au moins l'un des chien arrive entre le premier et dernier jour d'un mois donné
        # - Dont au moins l'un des chien part entre le premier et le dernier jour de ce mois
        # - Dont l'intervalle entre son arrivée et son départ comprend à la fois le premier et le dernier jour de ce mois
        reservations = Reservations.objects.filter(dog_1_arrival__gte=first_day, dog_1_arrival__lte=last_day) | (
                        Reservations.objects.filter(dog_1_departure__gte=first_day, dog_1_departure__lte=last_day)) | (
                        Reservations.objects.filter(dog_1_arrival__lt=first_day, dog_1_departure__gt=last_day)) | (
                        Reservations.objects.filter(dog_2_arrival__gte=first_day, dog_2_arrival__lte=last_day)) | (
                        Reservations.objects.filter(dog_2_departure__gte=first_day, dog_2_departure__lte=last_day)) | (
                        Reservations.objects.filter(dog_2_arrival__lt=first_day, dog_2_departure__gt=last_day)) | (
                        Reservations.objects.filter(dog_3_arrival__gte=first_day, dog_3_arrival__lte=last_day)) | (
                        Reservations.objects.filter(dog_3_departure__gte=first_day, dog_3_departure__lte=last_day)) | (
                        Reservations.objects.filter(dog_3_arrival__lt=first_day, dog_3_departure__gt=last_day)) | (
                        Reservations.objects.filter(dog_4_arrival__gte=first_day, dog_4_arrival__lte=last_day)) | (
                        Reservations.objects.filter(dog_4_departure__gte=first_day, dog_4_departure__lte=last_day)) | (
                        Reservations.objects.filter(dog_4_arrival__lt=first_day, dog_4_departure__gt=last_day)) | (
                        Reservations.objects.filter(dog_5_arrival__gte=first_day, dog_5_arrival__lte=last_day)) | (
                        Reservations.objects.filter(dog_5_departure__gte=first_day, dog_5_departure__lte=last_day)) | (
                        Reservations.objects.filter(dog_5_arrival__lt=first_day, dog_5_departure__gt=last_day))

        if build_array:
            days_of_month = [make_aware(datetime.datetime(year, month, day)) for day in range(1, num_days+1)]
            return {'reservations': reservations, 'days_of_month': days_of_month}

        else:
            return {'reservations': reservations, 'first_day': first_day, 'last_day': last_day}
