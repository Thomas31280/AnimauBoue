from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.timezone import make_aware
from django.utils import timezone
import datetime, calendar, pytz

from .forms import ConnectionForm, UpdateDataForm, AddClientForm, SelectParkAndClientForm, DogForm, SelectTimeFrameForm, AddDog
from django.contrib.auth.models import User
from administration.models import Clients, Dogs, Parks, Reservations

def index(request):
    template = loader.get_template('administration/index.html')
    return HttpResponse(template.render(request=request))


def connect_admin_space(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ConnectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user = authenticate(username=form.cleaned_data['userName'],
                                email=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])    # On va utiliser la méthode authenticate() pour vérifier le jeu de données d'identification. La méthode renvoie None si aucun moteur n'accpete l'authentification
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Vous avez été connecté avec succès')
                # redirect to a new URL:
                return HttpResponseRedirect('/connect_admin_space')
            
            else:
                messages.error(request, "Il semblerait que vos informations soient incorrectes. Nous n'avons pas pu vous connecter")
                return HttpResponseRedirect('/connect_admin_space')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = ConnectionForm()

    return render(request, 'administration/admin_connect_space.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès')
    return HttpResponseRedirect('/connect_admin_space')


@login_required
def update_profile_interface(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        current_datas = ConnectionForm(request.POST)
        new_datas = UpdateDataForm(request.POST)
        # check whether it's valid:
        if current_datas.is_valid() and new_datas.is_valid():
            # process the data in form.cleaned_data as required
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

                    messages.success(request, 'Vos information ont bien été mises à jour. Veuillez vous connecter')
                    # redirect to a new URL:
                    return HttpResponseRedirect('/connect_admin_space')
                
                else:
                    messages.error(request, "Vos deux nouveaux mots de passe ne correspondent pas. Veuillez réessayer")
                    return HttpResponseRedirect('/update_profile_interface')
            
            else:
                messages.error(request, "Erreur dans vos données de profil actuelles. Veuillez réessayer")
                return HttpResponseRedirect('/update_profile_interface')

    # if a GET (or any other method) we'll create a blank form
    else:
        current_datas = ConnectionForm()
        new_datas = UpdateDataForm()

    return render(request, 'administration/update_profile.html', {'current_datas': current_datas, 'new_datas': new_datas})


@user_passes_test(lambda u: u.is_superuser)
def administration_interface(request):
    template = loader.get_template('administration/administration_interface.html')
    return HttpResponse(template.render(request=request))


@user_passes_test(lambda u: u.is_superuser)
def parks_availability(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        park_to_update = request.POST.get('park')
        # if park_to_update has value:
        if park_to_update:
            update = Parks.objects.get(id=park_to_update)
            
            if update.availability:                                                                # On check le field availability de l'instace de Parks, afin de changer ce booléen en fonction de sa valeur actuelle
                update.availability = False
                update.save()
            
            else:
                update.availability = True
                update.save()
            
            messages.success(request, 'Le statut du parc '+update.name+' a été mis à jour avec succès')
            return HttpResponseRedirect('/parks_availability')

    # if a GET (or any other method) we'll just pass all the Parks instances to the template in a dict
    else:
        parks = Parks.objects.all().order_by('id')                                                 # On pense bien à ordonner les querysets pour avoir une liste toujours prévisible !

    return render(request, 'administration/parks_availability.html', {'parks': parks})


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
        # redirect to a new URL:
        return HttpResponseRedirect('/clients_profiles/')


@user_passes_test(lambda u: u.is_superuser)
def add_client_form(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        add_client_form = AddClientForm(request.POST)
        # check whether it's valid:
        if add_client_form.is_valid():
            
            datas = add_client_form.cleaned_data
            
            # process the data in form.cleaned_data as required
            Clients(first_name=datas['firstName'], name=datas['name'],
                    phone=datas['phone'], email=datas['email']).save()
            messages.success(request, 'Le client a bien été enregistré en base de données !')
            
            # redirect to a new URL:
            return HttpResponseRedirect('/clients_profiles/')
        
        else:
            messages.error(request, 'Un problème est survenu. Veuillez vérifier la validité de vos informations')
            return HttpResponseRedirect('/add_client_form/')

    # if a GET (or any other method) we'll create a blank form
    else:
        add_client_form = AddClientForm()

    return render(request, 'administration/add_client_form.html', {'add_client_form': add_client_form})


"""
Pour chercher un client, pouvoir le sélectionner et fournir
les formulaires de réservation
"""
@user_passes_test(lambda u: u.is_superuser)
def reservation_form(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        search = request.POST.get("recherche_client")
        
        # On va chercher le client en base de données, en utilisant bien la méthode __icontains pour rendre la recherche insensible à la casse et faire ressortir les résultats qui contiennent la recherche sans être exactement identiques
        clients = Clients.objects.filter(first_name__icontains=search) | Clients.objects.filter(name__icontains=search)
        
        if clients:
            #On prépare tous les formulaires nécessaires
            i=2
            fields = ['name', 'arrival_date', 'departure_date']

            park_and_client = SelectParkAndClientForm()
            dog_1 = DogForm()                                                      # On créé un formulaire basé sur forms.DogForm et on initialise le paramètre required de tous les fields ( sauf commentaries ) à True ( conséquence, les fields du premier formulaire seront obligatoire !!! )
            
            for field in fields:
                    dog_1.fields[field].required = True

            dog_2 = DogForm()                                                      # Puis on va succéssivement créer 4 autres forms basés sur forms.DogForm en mettant à jour les id de leurs fields à chaque fois ( on va se servir de ces id dans le template pour pouvoir set leurs paramètres required à True si le formulaire est display, et False s'il est hide !!! )
            dog_3 = DogForm()
            dog_4 = DogForm()
            dog_5 = DogForm()

            forms = [dog_2, dog_3, dog_4, dog_5]

            for form in forms:
                for field in fields:
                    form.fields[field].widget.attrs['id'] = field+"_dog"+str(i)
                    form.prefix = 'form'+str(i)
                i+=1
        
            return render(request, 'administration/reservation_form.html', {'park_and_client': park_and_client, 'clients': clients, 'dog_1': dog_1, 'dog_2': dog_2, 'dog_3': dog_3, 'dog_4': dog_4, 'dog_5': dog_5})
        
        else:
            messages.error(request, "Aucun client correspondant à votre recherche n'a été trouvé")
            return HttpResponseRedirect('/reservation_form/')

    else:

        return render(request, 'administration/reservation_form.html')


"""
Pour récupérer les formulaires de la vue reservation_form
et process les datas pour insérer une nouvelle réservation
dans la DB
"""
@user_passes_test(lambda u: u.is_superuser)
def add_reservation(request):

    # Si la requête est de type post, on va traiter les données des formulaires reçus
    if request.method == 'POST':
        # On récupère les formulaires
        park_and_client = SelectParkAndClientForm(request.POST)
        price = request.POST.get('price')
        # On utilise bien les préfixes des forms, car on a utilisé le même form plusieurs fois dans le template !
        dog_1 = DogForm(request.POST, prefix='form1')
        dog_2 = DogForm(request.POST, prefix='form2')
        dog_3 = DogForm(request.POST, prefix='form3')
        dog_4 = DogForm(request.POST, prefix='form4')
        dog_5 = DogForm(request.POST, prefix='form5')

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

                messages.success(request, "La réservation a bien été prise enregistrée !")
                return HttpResponseRedirect('/arrival-departure_interface/')

            else:
                messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
                return HttpResponseRedirect('/arrival-departure_interface/')


####A faire, vue non fonctionnelle !####
@user_passes_test(lambda u: u.is_superuser)
def arrival_and_departure_interface(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        time_frame = SelectTimeFrameForm(request.POST)
        # check whether it's valid:
        if time_frame.is_valid():
            # process the data in form.cleaned_data as required
            year = int(time_frame.cleaned_data['year'])
            month = int(time_frame.cleaned_data['month'])
            num_days = calendar.monthrange(year, month)[1]
            # On détermine le premier et dernier jour du mois, en utilisant le module datetime pour créer un objet de type datetime, et en utilisant sur cet objet la méthode django make_aware, qui permet de donner à l'objet datetime un attribut .tzinfo, qui contient des informations sur la timezone. Sans cela, il serait impossible de faire une compraison avec les datetimes présents en base de données
            first_day = make_aware(datetime.datetime(year, month, 1))
            last_day = make_aware(datetime.datetime(year, month, num_days))
            
            reservations = Reservations.objects.filter(dog_1_arrival__gte=first_day, dog_1_arrival__lte=last_day) | (
                           Reservations.objects.filter(dog_1_departure__gte=first_day, dog_1_departure__lte=last_day)) | (
                           Reservations.objects.filter(dog_2_arrival__gte=first_day, dog_2_arrival__lte=last_day)) | (
                           Reservations.objects.filter(dog_2_departure__gte=first_day, dog_2_departure__lte=last_day)) | (
                           Reservations.objects.filter(dog_3_arrival__gte=first_day, dog_3_arrival__lte=last_day)) | (
                           Reservations.objects.filter(dog_3_departure__gte=first_day, dog_3_departure__lte=last_day)) | (
                           Reservations.objects.filter(dog_4_arrival__gte=first_day, dog_4_arrival__lte=last_day)) | (
                           Reservations.objects.filter(dog_4_departure__gte=first_day, dog_4_departure__lte=last_day)) | (
                           Reservations.objects.filter(dog_5_arrival__gte=first_day, dog_5_arrival__lte=last_day)) | (
                           Reservations.objects.filter(dog_5_departure__gte=first_day, dog_5_departure__lte=last_day))

            if reservations:
                parks = Parks.objects.all().order_by('id')
                # On créé une liste de tous les datetime de la période sélectionnée
                days_of_month = [make_aware(datetime.datetime(year, month, day)) for day in range(1, num_days+1)]

                return render(request, 'administration/arrival-departure_interface.html', {'reservations': reservations, 'days_of_month': days_of_month, 'time_frame': time_frame, 'parks': parks})

            else:
                messages.error(request, "Aucune réservation n'a été trouvée pour cette période")
                return HttpResponseRedirect('/arrival-departure_interface/')

    # if a GET (or any other method) we'll create a blank form
    else:
        time_frame = SelectTimeFrameForm()
    return render(request, 'administration/arrival-departure_interface.html', {'time_frame': time_frame})


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
def update_client(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        update = AddClientForm(request.POST)
        client_id = request.POST.get('client_id')                                                  # On récupère les inputs cachés ( qui permettent d'identifier le client à update )
        client_phone = request.POST.get('current_phone')
        client = Clients.objects.get(id=client_id)
        
        if client.phone == client_phone:                                                           # On vérifie que le couple de données est bien cohérent ( pour prévenir les actions frauduleuses côté HTML )
            # check whether it's valid:
            if update.is_valid():
                # process the data in form.cleaned_data as required
                client.first_name = update.cleaned_data['firstName']
                client.name = update.cleaned_data['name']
                client.email = update.cleaned_data['email']
                client.phone = update.cleaned_data['phone']
                client.save()

                messages.success(request, 'Le profil client a été mis à jour avec succès')
                # redirect to a new URL:
                return HttpResponseRedirect('/clients_profiles/')            
            
            else:
                messages.error(request, 'Il semblerait que les informations soient incorrectes. Processus interrompu')
                # redirect to a new URL:
                return HttpResponseRedirect('/client/?client='+client_id)
        
        else:
            messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
            return HttpResponseRedirect('/clients_profiles/')

    # if a GET (or any other method) we'll create a blank form
    else:
        client_id = request.GET.get('client')
        client_phone = request.GET.get('client_phone')
        client = Clients.objects.get(id=client_id)
        
        if client.phone == '+'+client_phone:
            update = AddClientForm()

            update.fields['firstName'].initial = client.first_name
            update.fields['name'].initial = client.name
            update.fields['phone'].initial = client.phone
            update.fields['email'].initial = client.email

            return render(request, 'administration/update_client.html', {'client': client, 'update': update})
        
        else:
            messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
            return HttpResponseRedirect('/clients_profiles/')


@user_passes_test(lambda u: u.is_superuser)
def add_dog(request):
        
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        dog_form = AddDog(request.POST)
        client_id = request.POST.get('client_id')                                                  # On récupère les inputs cachés ( qui permettent d'identifier le client à update )
        client_phone = request.POST.get('client_phone')
        client = Clients.objects.get(id=client_id)
        
        if client.phone == client_phone:                                                           # On vérifie que le couple de données est bien cohérent ( pour prévenir les actions frauduleuses côté HTML )
            # check whether it's valid:
            if dog_form.is_valid():
                # process the data in form.cleaned_data as required
                Dogs(name=dog_form.cleaned_data['name'], owner=client).save()

                messages.success(request, 'Nouveau chien ajouté avec succès')
                # redirect to a new URL:
                return HttpResponseRedirect('/client/?client='+client_id)
        
        else:
            messages.error(request, "Nous suspectons une action malveillante de votre part. Le processus a été interrompu")
            return HttpResponseRedirect('/clients_profiles/')

    # if a GET (or any other method) we'll create a blank form
    else:
        client_id = request.GET.get('client')
        client_phone = request.GET.get('client_phone')
        client = Clients.objects.get(id=client_id)
        dogs = Dogs.objects.filter(owner=client_id)
        
        if client.phone == '+'+client_phone:
            dog_form = AddDog()

            return render(request, 'administration/add_dog.html', {'client': client, 'dog_form': dog_form, 'dogs': dogs})
        
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


@user_passes_test(lambda u: u.is_superuser)
def update_reservation(request):

    # Si la requête est de type post, on va traiter les données des formulaires reçus
    if request.method == 'POST':
        # On récupère les formulaires
        park_and_client = SelectParkAndClientForm(request.POST)
        price = request.POST.get('price')
        client_id = request.POST.get('client')
        client = Clients.objects.get(id=client_id)
        reservation_id = request.POST.get('reservation')
        reservation = Reservations.objects.get(id=reservation_id)
        # On utilise bien les préfixes des forms, car on a utilisé le même form plusieurs fois dans le template !
        dog_1 = DogForm(request.POST, prefix='form1')
        dog_2 = DogForm(request.POST, prefix='form2')
        dog_3 = DogForm(request.POST, prefix='form3')
        dog_4 = DogForm(request.POST, prefix='form4')
        dog_5 = DogForm(request.POST, prefix='form5')

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

    else:
        reservation_id = request.GET.get('reservation')
        client_phone = request.GET.get('client_phone')
        reservation = Reservations.objects.get(id=reservation_id)

        if reservation.client.phone == '+'+client_phone:
            #On prépare tous les formulaires nécessaires
            # On génère un formulaire à partir de SelectParkAndClientForm et on set la valeur initiale du field park au nom du parc associé à la réservation à update
            park_and_client = SelectParkAndClientForm()
            park_and_client.fields['park'].initial = reservation.park.id
            park_and_client.fields['client_id'].initial = 0
            
            dog_1 = DogForm()
            dog_2 = DogForm()
            dog_3 = DogForm()
            dog_4 = DogForm()
            dog_5 = DogForm()

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
