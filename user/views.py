from django.shortcuts import render
from administration.models import Parks
from administration.mixins import PlanningNStats


class ConsultAvailability(PlanningNStats):
    template_name = 'user/consult_availability.html'

    def get(self, request):
        time_frame = self.form_class()
        return render(request, self.template_name, {'time_frame': time_frame})

    def post(self, request):
        time_frame = self.form_class(request.POST)
        # Check whether it's valid:
        if time_frame.is_valid():
            # On envoie le formulaire valide dans la méthode "reservations_in_interval" de la classe mère "planning_n_stats"
            planning = self.reservations_in_interval(time_frame, True)
            parks = Parks.objects.filter(availability=True).order_by('id')
            month_availability = {}

            for day in planning['days_of_month']:
                availability_for_this_day = {}
                for park in parks:
                    for reservation in planning['reservations']:
                        # On vérifie si la réservation est associée au parc actuellement sélectionné dans la boucle
                        if reservation.park.id == park.id:
                            # Si c'est le cas, on va vérifier, pour chaque chien de la réservation, si la date actuellement sélectionnée dans la boucle est comprise entre son arrivée (incluse) et son départ (inclus). Si c'est le cas, c'est que le parc est occupé par au moins un chien. Dans ce cas, on va créer un élément dans le dictionaire availability_for_this_day ayant pour clé la valeur actuelle de park et pour valeur associée le booléen False
                            if reservation.dog_1_arrival.date() <= day.date() and day.date() <= reservation.dog_1_departure.date():
                                availability_for_this_day[park] = False

                            elif reservation.dog_2 and reservation.dog_2_arrival.date() <= day.date() and day.date() <= reservation.dog_2_departure.date():
                                availability_for_this_day[park] = False

                            elif reservation.dog_3 and reservation.dog_3_arrival.date() <= day.date() and day.date() <= reservation.dog_3_departure.date():
                                availability_for_this_day[park] = False

                            elif reservation.dog_4 and reservation.dog_4_arrival.date() <= day.date() and day.date() <= reservation.dog_4_departure.date():
                                availability_for_this_day[park] = False

                            elif reservation.dog_5 and reservation.dog_5_arrival.date() <= day.date() and day.date() <= reservation.dog_5_departure.date():
                                availability_for_this_day[park] = False

                    # A la fin du processus, on va vérifier l'existence dans availability_for_this_day d'un élément ayant pour clé la valeur actuelle de park
                    try:
                        availability_for_this_day[park]

                    # Si un tel élément n'existe pas, alors c'est qu'il n'a pas été créé ( car aucune réservation ne concerne ce parc à cette date ), et on peut donc en déduire qu'il est nécessairement libre. On créé donc un élément avec cette clé associée au booléen True, car il est libre
                    except Exception:
                        availability_for_this_day[park] = True

                month_availability[day] = availability_for_this_day

        return render(request, self.template_name, {'time_frame': time_frame, 'planning': month_availability, 'parks': parks})
