from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.timezone import make_aware
from django.utils import timezone
from django.views import View
import datetime, calendar, pytz

from .forms import ConnectionForm, UpdateDataForm, AddClientForm, SelectParkAndClientForm, DogForm, SelectTimeFrameForm, AddDog
from django.contrib.auth.models import User
from administration.models import Clients, Dogs, Parks, Reservations
from administration.mixins import SuperUserRequired, PlanningNStats


def index(request):
    template = loader.get_template('administration/index.html')
    return HttpResponse(template.render(request=request))


#######################################################################################
#####################################Admin_account#####################################
#######################################################################################
class ConnectAdminSpace(View):
    template_name = 'administration/admin_connect_space.html'
    form_class = ConnectionForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data as required
            user = authenticate(username=form.cleaned_data['userName'],
                                email=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])    # On va utiliser la méthode authenticate() pour vérifier le jeu de données d'identification. La méthode renvoie None si aucun moteur n'accpete l'authentification
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Vous avez été connecté avec succès')
                # redirect to a new URL:
                return HttpResponseRedirect('/connect_admin_space/')
            
            else:
                messages.error(request, "Il semblerait que vos informations soient incorrectes. Nous n'avons pas pu vous connecter")
                return HttpResponseRedirect('/connect_admin_space/')


class UpdateProfile(View):
    current_datas_class = ConnectionForm
    new_datas_class = UpdateDataForm
    template_name = 'administration/update_profile.html'

    def get(self, request):
        current_datas = self.current_datas_class()
        new_datas = self.new_datas_class()
        return render(request, self.template_name, {'current_datas': current_datas, 'new_datas': new_datas})
    
    def post(self, request):
        current_datas = self.current_datas_class(request.POST)
        new_datas = self.new_datas_class(request.POST)

        if current_datas.is_valid() and new_datas.is_valid():
            # Process the data in form.cleaned_data as required
            username_check = (request.user.username == current_datas.cleaned_data['userName'])     # Checking de la validité des infos passées au formulaire. On utilise la méthode check_password sur l'instance user afin de vérifier la validité du mot de passe de manière sécurisée !
            email_check = (request.user.email == current_datas.cleaned_data['email'])
            password_check = request.user.check_password(current_datas.cleaned_data['password'])

            if username_check and email_check and password_check:

                if new_datas.cleaned_data['new_password'] == new_datas.cleaned_data['new_password_confirm']: # Checking de la correspondance des deux passwords
                    user_to_update = User.objects.get(id=request.user.id)                                    # On trouve l'utilisateur concerné dans la table, et on procède à la mise à jour de ses informations. On utilise bien la méthode Django set_password() pour le MDP !!
                    user_to_update.username = new_datas.cleaned_data['new_username']
                    user_to_update.email = new_datas.cleaned_data['new_email']
                    user_to_update.set_password(new_datas.cleaned_data['new_password'])
                    user_to_update.save()

                    messages.success(request, 'Vos informations ont bien été mises à jour. Veuillez vous connecter')
                    return HttpResponseRedirect('/connect_admin_space/')
                
                else:
                    messages.error(request, "Vos deux nouveaux mots de passe ne correspondent pas. Veuillez réessayer")
                    return HttpResponseRedirect('/update_profile/')
            
            else:
                messages.error(request, "Erreur dans vos données de profil actuelles. Veuillez réessayer")
                return HttpResponseRedirect('/update_profile/')


@user_passes_test(lambda u: u.is_superuser)
def administration_interface(request):
    template = loader.get_template('administration/administration_interface.html')
    return HttpResponse(template.render(request=request))


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès')
    return HttpResponseRedirect('/connect_admin_space')


######################################################################################
#####################################Parks Status#####################################
######################################################################################
class ParksAvailability(View, SuperUserRequired):
    template_name = 'administration/parks_availability.html'

    def get(self, request):
        if SuperUserRequired.super_user(self):
            parks = Parks.objects.all().order_by('id')                        # On pense bien à ordonner les querysets pour avoir une liste toujours prévisible !
            return render(request, self.template_name, {'parks': parks})
    
    def post(self, request):
        if SuperUserRequired.super_user(self):
            park_to_update = request.POST.get('park')

            if park_to_update:
                update = Parks.objects.get(id=park_to_update)
                
                if update.availability:                                       # On check le field availability de l'instace de Parks, afin de changer ce booléen en fonction de sa valeur actuelle
                    update.availability = False
                    update.save()
                
                else:
                    update.availability = True
                    update.save()
                
                messages.success(request, 'Le statut du parc '+update.name+' a été mis à jour avec succès')
                return HttpResponseRedirect('/parks_availability/')


#################################################################################
#####################################Clients#####################################
#################################################################################
class AddClientForm(View, SuperUserRequired):
    template_name = 'administration/add_client_form.html'
    form_class = AddClientForm

    def get(self, request):
        if SuperUserRequired.super_user(self):
            add_client_form = self.form_class()
            return render(request, self.template_name, {'add_client_form': add_client_form})
    
    def post(self, request):
        if SuperUserRequired.super_user(self):
            add_client_form = self.form_class(request.POST)
            
            if add_client_form.is_valid():
                datas = add_client_form.cleaned_data
                
                Clients(first_name=datas['firstName'], name=datas['name'],
                        phone=datas['phone'], email=datas['email']).save()

                messages.success(request, 'Le client a bien été enregistré en base de données !')
                return HttpResponseRedirect('/clients_profiles/')
            
            else:
                messages.error(request, 'Un problème est survenu. Veuillez vérifier la validité de vos informations')
                return HttpResponseRedirect('/add_client_form/')


class UpdateClient(View, SuperUserRequired):
    form_class = AddClientForm

    def get(self, request):
        if SuperUserRequired.super_user(self):
            client_id = request.GET.get('client')
            client_phone = request.GET.get('client_phone')
            client = Clients.objects.get(id=client_id)
            
            if client.phone == '+'+client_phone:
                update = self.form_class()

                update.fields['firstName'].initial = client.first_name
                update.fields['name'].initial = client.name
                update.fields['phone'].initial = client.phone
                update.fields['email'].initial = client.email

                return render(request, 'administration/update_client.html', {'client': client, 'update': update})
            
            else:
                messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
                return HttpResponseRedirect('/clients_profiles/')
        
    def post(self, request):
        if SuperUserRequired.super_user(self):
            update = self.form_class(request.POST)
            client_id = request.POST.get('client_id')                                                  # On récupère les inputs cachés ( qui permettent d'identifier le client à update )
            client_phone = request.POST.get('current_phone')
            client = Clients.objects.get(id=client_id)
            
            if client.phone == client_phone:                                                           # On vérifie que le couple de données est bien cohérent ( pour prévenir les actions frauduleuses côté HTML )
                # Check whether it's valid:
                if update.is_valid():
                    # Process the data in form.cleaned_data as required
                    client.first_name = update.cleaned_data['firstName']
                    client.name = update.cleaned_data['name']
                    client.email = update.cleaned_data['email']
                    client.phone = update.cleaned_data['phone']
                    client.save()

                    messages.success(request, 'Le profil client a été mis à jour avec succès')
                    return HttpResponseRedirect('/clients_profiles/')            
                
                else:
                    messages.error(request, 'Il semblerait que les informations soient incorrectes. Processus interrompu')
                    return HttpResponseRedirect('/client/?client='+client_id)
            
            else:
                messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
                return HttpResponseRedirect('/clients_profiles/')


@user_passes_test(lambda u: u.is_superuser)
def client_reservations(request):
    
    client_id = request.GET.get('client')
    client_phone = request.GET.get('client_phone')
    client = Clients.objects.get(id=client_id)
    
    if client.phone == '+'+client_phone:
        # On ordonne les résultats du plus récent au plus ancien
        reservations = Reservations.objects.filter(client=client_id).order_by('-dog_1_arrival')

        return render(request, 'administration/client_reservations.html', {'reservations': reservations, 'client': client})
    else:
        messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
        return HttpResponseRedirect('/clients_profiles/')


@user_passes_test(lambda u: u.is_superuser)
def delete_client(request):
    
    client_id = request.POST.get('client_id')
    client_phone = request.POST.get('client_phone')
    client = Clients.objects.get(id=client_id)

    if client.phone == client_phone:                                                               # On vérifie la cohérence des deux fields passés à la vue. Si cette correspondance est mauvaise, cela signifie que l'utilisateur a tenté de modifier la valeur des inputs du formulaire dans le code HTML
        client.delete()
        messages.success(request, "Le client a bien été supprimé de la base de données")
        return HttpResponseRedirect('/clients_profiles/')
    
    else:
        messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
        return HttpResponseRedirect('/clients_profiles/')


@user_passes_test(lambda u: u.is_superuser)
def clients_profiles(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        search = request.POST.get("recherche_client")

        # On va chercher le client en base de données, en utilisant bien la méthode __icontains pour rendre la recherche insensible à la casse et faire ressortir les résultats qui contiennent la recherche sans être exactement identiques
        clients = Clients.objects.filter(first_name__icontains=search) | Clients.objects.filter(name__icontains=search)

        if clients:
            clients_list = clients

        else:
            clients_list = Clients.objects.all()
            messages.error(request, "Aucun client correspondant à votre recherche n'a été trouvé en base de données")

    else:
        clients_list = Clients.objects.all()                                                       # Liste de tous les clients de la DB

    paginator = Paginator(clients_list, 18)                                                        # On utilise paginator sur la liste
    page_number = request.GET.get('page')                                                          # On récupère le numéro de la page actuelle dans l'URL
    page_objs = paginator.get_page(page_number)                                                    # On définit une variable page_objs qui va stocker les éléments de la page actuelle de l'instance de Paginator paginator précédemment créée

    return render(request, 'administration/clients.html', {'page_objs': page_objs})                # On retourne le bon template et on lui passe le dictionnaire contenant les objets de la page ( page_objs )


@user_passes_test(lambda u: u.is_superuser)
def client(request):
    client_id = request.GET.get('client')
    
    try:                                                                                           # On tente de dérouler le scénario dans lequel le client est présent en base de données
        client = Clients.objects.get(id=client_id)
        dogs = Dogs.objects.filter(owner=client_id)
        return render(request, 'administration/client_profile.html', {'client': client, 'dogs': dogs})
    
    except Exception:
        messages.error(request, "Le client demandé n'existe pas. Veuillez en choisir un parmi la liste ci-dessous")    
        return HttpResponseRedirect('/clients_profiles/')


######################################################################################
#####################################Reservations#####################################
######################################################################################
class Reservations(View, SuperUserRequired):
    template_name = 'administration/reservation_form.html'
    dog_form_class = DogForm
    park_n_client_form_class = SelectParkAndClientForm


"""
Pour chercher un client, pouvoir le sélectionner et fournir
les formulaires de réservation
"""
class ReservationForm(Reservations):

    def get(self, request):
        if SuperUserRequired.super_user(self):
            return render(request, self.template_name)
    
    def post(self, request):
        if SuperUserRequired.super_user(self):
            search = request.POST.get("recherche_client")
            
            # On va chercher le client en base de données, en utilisant bien la méthode __icontains pour rendre la recherche insensible à la casse et faire ressortir les résultats qui contiennent la recherche sans être exactement identiques
            clients = Clients.objects.filter(first_name__icontains=search) | Clients.objects.filter(name__icontains=search)
            
            if clients:
                # On prépare tous les formulaires nécessaires
                i=2
                fields = ['name', 'arrival_date', 'departure_date']

                park_and_client = self.park_n_client_form_class()
                dog_1 = self.dog_form_class()                                           # On créé un formulaire basé sur forms.DogForm et on initialise le paramètre required de tous les fields ( sauf commentaries ) à True ( conséquence, les fields du premier formulaire seront obligatoire !!! )
                
                for field in fields:
                        dog_1.fields[field].required = True

                dog_2 = self.dog_form_class()                                            # Puis on va succéssivement créer 4 autres forms basés sur forms.DogForm en mettant à jour les id de leurs fields à chaque fois ( on va se servir de ces id dans le template pour pouvoir set leurs paramètres required à True si le formulaire est display, et False s'il est hide !!! )
                dog_3 = self.dog_form_class()
                dog_4 = self.dog_form_class()
                dog_5 = self.dog_form_class()

                forms = [dog_2, dog_3, dog_4, dog_5]

                for form in forms:
                    for field in fields:
                        form.fields[field].widget.attrs['id'] = field+"_dog"+str(i)
                        form.prefix = 'form'+str(i)
                    i+=1
            
                return render(request, self.template_name, {'park_and_client': park_and_client, 'clients': clients, 'dog_1': dog_1, 'dog_2': dog_2, 'dog_3': dog_3, 'dog_4': dog_4, 'dog_5': dog_5})
            
            else:
                messages.error(request, "Aucun client correspondant à votre recherche n'a été trouvé")
                return HttpResponseRedirect('/reservation_form/')


"""
Pour récupérer les formulaires de la vue reservation_form
et process les datas pour insérer une nouvelle réservation
dans la DB
"""
class AddReservation(Reservations):

    def post(self, request):
        if SuperUserRequired.super_user(self):
            # On récupère les formulaires
            park_and_client = self.park_n_client_form_class(request.POST)
            price = request.POST.get('price')
            # On utilise bien les préfixes des forms, car on a utilisé le même form plusieurs fois dans le template !
            dog_1 = self.dog_form_class(request.POST, prefix='form1')
            dog_2 = self.dog_form_class(request.POST, prefix='form2')
            dog_3 = self.dog_form_class(request.POST, prefix='form3')
            dog_4 = self.dog_form_class(request.POST, prefix='form4')
            dog_5 = self.dog_form_class(request.POST, prefix='form5')

            # On check que tous les forms sont valides, et on process les datas des forms si c'est ok
            if park_and_client.is_valid() and dog_1.is_valid() and dog_2.is_valid() and dog_3.is_valid() and dog_4.is_valid() and dog_5.is_valid():
                # On prépare tous les éléments dont on va avoir besoin
                dogs_forms = [dog_1.cleaned_data, dog_2.cleaned_data, dog_3.cleaned_data, dog_4.cleaned_data, dog_5.cleaned_data]
                client = Clients.objects.get(id=park_and_client.cleaned_data['client_id'])
                park = Parks.objects.get(id=park_and_client.cleaned_data['park'])
                datas = {'price': price}
                
                if client and park:
                    datas['client'] = client
                    datas['park'] = park
                    i=1
                    for dog_form in dogs_forms:
                        # Sous entendu 'si le formulaire n'est pas vide', car name est set à required = True
                        if dog_form['name']:
                            try:
                                dog = Dogs.objects.get(name__iexact=dog_form['name'], owner=client)
                                if dog:
                                    for field in dog_form:
                                        if field != 'name':
                                            datas[field+'_dog_'+str(i)] = dog_form[field]
                                        else:
                                            datas['dog_'+str(i)] = dog

                            except Exception:
                                messages.error(request, "Au moins l'un des chiens référencés lors de la réservation n'est pas référencé en base de données. Veuillez vérifier vos informations")
                                return HttpResponseRedirect('/reservation_form/')
                        
                        else:
                            for field in dog_form:
                                if field != 'name':
                                    datas[field+'_dog_'+str(i)] = dog_form[field]
                                else:
                                    datas['dog_'+str(i)] = None
                        i+=1

                    # Maintenant que nous avons récupéré toutes les données dans un dictionnaire, on va les insérer dans la table
                    Reservations(price=datas['price'], client=datas['client'], park=datas['park'], dog_1=datas['dog_1'],
                                dog_2=datas['dog_2'], dog_3=datas['dog_3'], dog_4=datas['dog_4'], dog_5=datas['dog_5'],
                                dog_1_arrival=datas['arrival_date_dog_1'], dog_2_arrival=datas['arrival_date_dog_2'],
                                dog_3_arrival=datas['arrival_date_dog_3'], dog_4_arrival=datas['arrival_date_dog_4'],
                                dog_5_arrival=datas['arrival_date_dog_5'], dog_1_departure=datas['departure_date_dog_1'],
                                dog_2_departure=datas['departure_date_dog_2'], dog_3_departure=datas['departure_date_dog_3'],
                                dog_4_departure=datas['departure_date_dog_4'], dog_5_departure=datas['departure_date_dog_5']).save()

                    messages.success(request, "La réservation a bien été enregistrée !")
                    return HttpResponseRedirect('/arrival-departure_interface/')

                else:
                    messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
                    return HttpResponseRedirect('/arrival-departure_interface/')


class UpdateReservation(Reservations):
    
    def get(self, request):
        if SuperUserRequired.super_user(self):
            reservation_id = request.GET.get('reservation')
            client_phone = request.GET.get('client_phone')
            reservation = Reservations.objects.get(id=reservation_id)

            if reservation.client.phone == '+'+client_phone:
                # On prépare tous les formulaires nécessaires
                # On génère un formulaire à partir de SelectParkAndClientForm et on set la valeur initiale du field park au nom du parc associé à la réservation à update
                park_and_client = self.park_n_client_form_class()
                park_and_client.fields['park'].initial = reservation.park.id
                park_and_client.fields['client_id'].initial = 0
                
                dog_1 = self.dog_form_class()
                dog_2 = self.dog_form_class()
                dog_3 = self.dog_form_class()
                dog_4 = self.dog_form_class()
                dog_5 = self.dog_form_class()

                i=2
                fields = ['name', 'arrival_date', 'departure_date']
                forms = [dog_1, dog_2, dog_3, dog_4, dog_5]
                dogs = [reservation.dog_1, reservation.dog_2, reservation.dog_3, reservation.dog_4, reservation.dog_5]
                arrivals = [reservation.dog_1_arrival, reservation.dog_2_arrival, reservation.dog_3_arrival, reservation.dog_4_arrival, reservation.dog_5_arrival]
                departures = [reservation.dog_1_departure, reservation.dog_2_departure, reservation.dog_3_departure, reservation.dog_4_departure, reservation.dog_5_departure]
                
                for field in fields:
                    dog_1.fields[field].required = True

                # On attribue des préfixes distincts aux forms créés à partir de la même base, afin de pouvoir les récupérer correctement par la suite
                for form in forms:
                    if form != forms[0]:
                        for field in fields:
                            form.fields[field].widget.attrs['id'] = field+"_dog"+str(i)
                        form.prefix = 'form'+str(i)
                        i+=1

                # On va déterminer le delta entre l'heure locale pour une date donnée et l'heure UTC+0 afin de déterminer de combien il faut incrémenter le .initial des champs arrival_date et departure_date des formulaires. On rappel que lorsque l'on conculte un objet de tipe datetime aware depuis une table, bien qu'il continue à être aware lorsqu'on l'appel dans une vue, quand on consulte sa valeur, elle est retournée sans prendre en compte la timezone. Il faut donc faire en sorte de retourner à une valeur prenant en compte la timezone...
                paris = pytz.timezone('Europe/Paris')

                # On va parcourir ces 4 listes en même temps, et set les valeurs initiales des fields des forms correctement
                for form, dog, arrival, departure in zip(forms, dogs, arrivals, departures):
                    if dog is not None:
                        arr = arrival
                        dep = departure
                        # Différence entre l'heure locale et l'heure UTC+0 pour les dates de départ et d'arrivée ( on ne retient que l'heure, qu'on convertit en int )
                        delta_arrival = int(str(paris.utcoffset(datetime.datetime(arr.year, arr.month, arr.day)))[0])
                        delta_departure = int(str(paris.utcoffset(datetime.datetime(dep.year, dep.month, dep.day)))[0])
                        form.fields['name'].initial = dog.name
                        form.fields['arrival_date'].initial = str(datetime.datetime(year=arr.year, month=arr.month, day=arr.day, hour=arr.hour+delta_arrival, minute=arr.minute))
                        form.fields['departure_date'].initial = str(datetime.datetime(year=dep.year, month=dep.month, day=dep.day, hour=dep.hour+delta_departure, minute=dep.minute))

                return render(request, 'administration/update_reservation.html', {'park_and_client': park_and_client, 'reservation': reservation, 'dog_1': dog_1, 'dog_2': dog_2, 'dog_3': dog_3, 'dog_4': dog_4, 'dog_5': dog_5})
            
            else:
                messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
                return HttpResponseRedirect('/clients_profiles/')

    def post(self, request):
        if SuperUserRequired.super_user(self):
            park_and_client = self.park_n_client_form_class(request.POST)
            price = request.POST.get('price')
            client_id = request.POST.get('client')
            client = Clients.objects.get(id=client_id)
            reservation_id = request.POST.get('reservation')
            reservation = Reservations.objects.get(id=reservation_id)
            # On utilise bien les préfixes des forms, car on a utilisé le même form plusieurs fois dans le template !
            dog_1 = self.dog_form_class(request.POST, prefix='form1')
            dog_2 = self.dog_form_class(request.POST, prefix='form2')
            dog_3 = self.dog_form_class(request.POST, prefix='form3')
            dog_4 = self.dog_form_class(request.POST, prefix='form4')
            dog_5 = self.dog_form_class(request.POST, prefix='form5')

            # On check que tous les forms sont valides, et on process les datas des forms si c'est ok
            if park_and_client.is_valid() and dog_1.is_valid() and dog_2.is_valid() and dog_3.is_valid() and dog_4.is_valid() and dog_5.is_valid():
                # On prépare tous les éléments dont on va avoir besoin
                dogs_forms = [dog_1.cleaned_data, dog_2.cleaned_data, dog_3.cleaned_data, dog_4.cleaned_data, dog_5.cleaned_data]
                park = Parks.objects.get(id=park_and_client.cleaned_data['park'])
                datas = {'price': price}
                
                if park and client_id and reservation.client == client:
                    datas['park'] = park
                    i=1
                    for dog_form in dogs_forms:
                        # Sous entendu 'si le formulaire n'est pas vide', car name est set à required = True
                        if dog_form['name']:
                            try:
                                dog = Dogs.objects.get(name__iexact=dog_form['name'], owner=client_id)
                                if dog:
                                    for field in dog_form:
                                        if field != 'name':
                                            datas[field+'_dog_'+str(i)] = dog_form[field]
                                        else:
                                            datas['dog_'+str(i)] = dog

                            except Exception:
                                messages.error(request, "Au moins l'un des chiens référencés lors de la réservation n'est pas référencé en base de données. Veuillez réessayer")
                                return HttpResponseRedirect('/client_reservations/?client='+client_id+'&client_phone='+str(client.phone))
                        
                        else:
                            for field in dog_form:
                                if field != 'name':
                                    datas[field+'_dog_'+str(i)] = dog_form[field]
                                else:
                                    datas['dog_'+str(i)] = None
                        i+=1

                    reservation.price = datas['price']
                    reservation.park = datas['park']
                    reservation.dog_1 = datas['dog_1']
                    reservation.dog_1_arrival = datas['arrival_date_dog_1']
                    reservation.dog_1_departure = datas['departure_date_dog_1']
                    reservation.dog_2 = datas['dog_2']
                    reservation.dog_2_arrival = datas['arrival_date_dog_2']
                    reservation.dog_2_departure = datas['departure_date_dog_2']
                    reservation.dog_3 = datas['dog_3']
                    reservation.dog_3_arrival = datas['arrival_date_dog_3']
                    reservation.dog_3_departure = datas['departure_date_dog_3']
                    reservation.dog_4 = datas['dog_4']
                    reservation.dog_4_arrival = datas['arrival_date_dog_4']
                    reservation.dog_4_departure = datas['departure_date_dog_4']
                    reservation.dog_5 = datas['dog_5']
                    reservation.dog_5_arrival = datas['arrival_date_dog_5']
                    reservation.dog_5_departure = datas['departure_date_dog_5']
                    reservation.save()

                    messages.success(request, "Vos modifications ont bien été prises en compte !")
                    return HttpResponseRedirect('/client_reservations/?client='+client_id+'&client_phone='+str(client.phone))
                
                else:
                    messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
                    return HttpResponseRedirect('/clients_profiles/')


@user_passes_test(lambda u: u.is_superuser)
def delete_reservation(request):
    
    reservation_id = request.POST.get('reservation_id')
    client = request.POST.get('client')
    reservation = Reservations.objects.get(id=reservation_id)

    if reservation.client.id == int(client):
        reservation.delete()
        messages.success(request, "La réservation a été supprimée avec succès")
        return HttpResponseRedirect('/client/?client='+client)
    
    else:
        messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
        return HttpResponseRedirect('/clients_profiles/')


#############################################################################################
#####################################Plannings and stats#####################################
#############################################################################################
class ArrivalAndDeparture(PlanningNStats):
    template_name = 'administration/arrival-departure_interface.html'
    
    def get(self, request):
        if SuperUserRequired.super_user(self):
            time_frame = self.form_class()
            return render(request, self.template_name, {'time_frame': time_frame})
    
    def post(self, request):
        if SuperUserRequired.super_user(self):
            time_frame = self.form_class(request.POST)
            # check whether it's valid:
            if time_frame.is_valid():
                # On envoie le formulaire valide dans la méthode "reservations_in_interval" de la classe mère "planning_n_stats"
                planning = self.reservations_in_interval(time_frame, True)            

                if planning['reservations']:
                    parks = Parks.objects.all().order_by('id')
                    return render(request, self.template_name, {'reservations': planning['reservations'], 'days_of_month': planning['days_of_month'], 'time_frame': time_frame, 'parks': parks})

                else:
                    messages.error(request, "Aucune réservation n'a été trouvée pour cette période")
                    return HttpResponseRedirect('/arrival-departure_interface/')


class Stats(PlanningNStats):
    template_name = 'administration/stats.html'

    def get(self, request):
        if SuperUserRequired.super_user(self):
            time_frame = self.form_class()
            return render(request, self.template_name, {'time_frame': time_frame})

    def post(self, request):
        if SuperUserRequired.super_user(self):
            time_frame = self.form_class(request.POST)

            if time_frame.is_valid():

                datas = self.reservations_in_interval(time_frame, False)
                reservations_time_frame = datas['reservations']
                first_day = datas['first_day']
                last_day = datas['last_day']
                
                # On initialise toutes les stats
                turnover = 0
                rate_of_occupation = 0
                nb_reservations = 0
                avg_duration = 0
                nb_days_occupied = 0
                
                if reservations_time_frame:
                    # On détermine d'office le nombre de réservations
                    nb_reservations = len(reservations_time_frame)

                    for reservation in reservations_time_frame:
                        dates = [reservation.dog_1_arrival, reservation.dog_1_departure, reservation.dog_2_arrival, reservation.dog_2_departure,
                                reservation.dog_3_arrival, reservation.dog_3_departure, reservation.dog_4_arrival, reservation.dog_4_departure,
                                reservation.dog_5_arrival, reservation.dog_5_departure]
                        
                        start = dates[0]
                        end = dates[1]
                        
                        for index in range(0, 9, 2):
                            # On navigue dans une liste de toutes les querysets :
                            # - Dont au moins l'un des chien arrive entre le premier et dernier jour d'un mois donné
                            # - Dont au moins l'un des chien part entre le premier et le dernier jour de ce mois
                            # - Dont l'intervalle entre son arrivée et son départ comprend à la fois le premier et le dernier jour de ce mois
                            # On souhaite maintenant définir, pour chacune d'entre elle, le nombre de jours dans l'intervalle formé par l'arrivée du premier chien et le départ du dernier qui se trouvent dans ce mois.
                            if dates[index] is not None:
                                if start < first_day:
                                    start = first_day
                                elif dates[index] < start:
                                    start = dates[index]
                                
                                if end > last_day:
                                    end = last_day
                                elif dates[index+1] > end:
                                    end = dates[index+1]

                        delta = end - start
                        nb_days_occupied += (delta.days + delta.seconds/86400)
                        
                        # Si, pour la réservation, le dernier chien à partir part à une date comprise dans le mois, on incrémente turnover du prix de la réservation
                        if end < last_day:
                            turnover += reservation.price

                    # On définit la durée moyenne d'une réservation
                    avg_duration = nb_days_occupied/nb_reservations
                    
                    # On détermine ensuite la durée d'un mois, et on va multiplier le résultat par le nombre de tous les parcs disponnibles
                    # ( donc le nombre de jours occupés maximum théorique ), puis diviser le nombre de jours occupés dans le mois par ce chiffre
                    # pour obtenir le pourcentage d'occupation des parcs.
                    month_duration = (last_day - first_day).days + (last_day - first_day).seconds/86400
                    rate_of_occupation = (nb_days_occupied/(month_duration*len(Parks.objects.filter(availability=True))))*100

                    stats = {'avg_duration': "{:.2f}".format(avg_duration), 'nb_days_occupied': "{:.2f}".format(nb_days_occupied), 'nb_reservations': nb_reservations, 'rate_of_occupation': "{:.2f}".format(rate_of_occupation), 'turnover': turnover, 'time_frame': time_frame}
                    return render(request, self.template_name, {'time_frame': time_frame, 'stats': stats})
                
                else:
                    messages.error(request, "Aucune réservation enregistrée pour cette période")
                    return HttpResponseRedirect('/stats/')


##############################################################################
#####################################Dogs#####################################
##############################################################################
class AddDog(View, SuperUserRequired):
    form_class = AddDog

    def get(self, request):
        if SuperUserRequired.super_user(self):
            client_id = request.GET.get('client')
            client_phone = request.GET.get('client_phone')
            client = Clients.objects.get(id=client_id)
            dogs = Dogs.objects.filter(owner=client_id)
            
            if client.phone == '+'+client_phone:
                dog_form = self.form_class()
                return render(request, 'administration/add_dog.html', {'client': client, 'dog_form': dog_form, 'dogs': dogs})
            
            else:
                messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
                return HttpResponseRedirect('/clients_profiles/')
    
    def post(self, request):
        if SuperUserRequired.super_user(self):
            dog_form = self.form_class(request.POST)
            client_id = request.POST.get('client_id')                                                  # On récupère les inputs cachés ( qui permettent d'identifier le client à update )
            client_phone = request.POST.get('client_phone')
            client = Clients.objects.get(id=client_id)
            
            if client.phone == client_phone:                                                           # On vérifie que le couple de données est bien cohérent ( pour prévenir les actions frauduleuses côté HTML )
                # Check whether it's valid:
                if dog_form.is_valid():
                    Dogs(name=dog_form.cleaned_data['name'], owner=client, transponder=dog_form.cleaned_data['transponder']).save()

                    messages.success(request, 'Nouveau chien ajouté avec succès')
                    return HttpResponseRedirect('/client/?client='+client_id)
                
                else:
                    messages.error(request, 'Format du numéro de transpondeur incorrect. Veuillez entrer exclusivement des chiffres')
                    return HttpResponseRedirect('/add_dog/?client='+client_id+'&client_phone='+client_phone)
            
            else:
                messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
                return HttpResponseRedirect('/clients_profiles/')


class UpdateDog(View, SuperUserRequired):
    form_class = AddDog

    def get(self, request):
        if SuperUserRequired.super_user(self):
            dog_id = request.GET.get('dog')
            owner_id = request.GET.get('owner')
            dog = Dogs.objects.get(id=dog_id)

            if dog.owner.id == int(owner_id):
                dog_form = self.form_class()
                dog_form.fields['name'].initial = dog.name
                dog_form.fields['name'].label = 'Nom du chien :'
                dog_form.fields['transponder'].initial = dog.transponder
                return render(request, 'administration/update_dog.html', {'dog': dog, 'owner': dog.owner, 'dog_form': dog_form})
            
            else:
                messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
                return HttpResponseRedirect('/clients_profiles/')
    
    def post(self, request):
        if SuperUserRequired.super_user(self):
            dog_id = request.POST.get('dog_id')
            owner_id = request.POST.get('owner_id')
            dog = Dogs.objects.get(id=dog_id)

            if dog.owner.id == int(owner_id):
                form = self.form_class(request.POST)
                
                if form.is_valid():
                    
                    dog.name = form.cleaned_data['name']
                    dog.transponder = form.cleaned_data['transponder']
                    dog.save()
                    
                    messages.success(request, 'Les informations de '+dog.name+' ont été mises à jour avec succès')
                    return HttpResponseRedirect('/client/?client='+owner_id)
            
            else:
                messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
                return HttpResponseRedirect('/clients_profiles/')


@user_passes_test(lambda u: u.is_superuser)
def delete_dog(request):

    dog_id = request.POST.get('dog_id')
    owner = request.POST.get('owner')
    dog = Dogs.objects.get(id=dog_id)

    if dog.owner.id == int(owner):                                                                 # On vérifie la cohérence des deux fields passés à la vue. Si cette correspondance est mauvaise, cela signifie que l'utilisateur a tenté de modifier la valeur des inputs du formulaire dans le code HTML
        dog.delete()
        messages.success(request, "Le chien a bien été supprimé de la base de données")
        return HttpResponseRedirect('/client/?client='+owner)
    
    else:
        messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
        return HttpResponseRedirect('/client/?client='+owner)
