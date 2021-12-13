from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import ConnectionForm, UpdateDataForm, AddClientForm, SelectParkAndClientForm, DogForm, SelectTimeFrameForm
from django.contrib.auth.models import User
from administration.models import Clients

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

def administration_interface(request):
    template = loader.get_template('administration/administration_interface.html')
    return HttpResponse(template.render(request=request))

def consult_parks_availability(request):
    template = loader.get_template('administration/parks_availability.html')
    return HttpResponse(template.render(request=request))

def clients_profiles(request):
    clients_list = Clients.objects.all()                                                           # Liste de tous les clients de la DB
    paginator = Paginator(clients_list, 18)                                                        # On utilise paginator sur la liste
    page_number = request.GET.get('page')                                                          # On récupère le numéro de la page actuelle dans l'URL
    page_objs = paginator.get_page(page_number)                                                    # On définit une variable page_objs qui va stocker les éléments de la page actuelle de l'instance de Paginator paginator précédemment créée

    return render(request, 'administration/clients.html', {'page_objs': page_objs})                # On retourne le bon template et on lui passe le dictionnaire contenant les objets de la page ( page_objs )

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

def reservation_form(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        park_and_client = SelectParkAndClientForm(request.POST)
        dog_1 = DogForm(request.POST)
        dog_2 = DogForm(request.POST)
        dog_3 = DogForm(request.POST)
        dog_4 = DogForm(request.POST)
        dog_5 = DogForm(request.POST)
        # check whether it's valid:
        if park_and_client.is_valid() and dog_1.is_valid() and dog_2.is_valid() and dog_3.is_valid() and dog_4.is_valid() and dog_5.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        
        i=2
        fields = ['name', 'commentaries', 'arrival_date', 'departure_date']

        park_and_client = SelectParkAndClientForm()
        dog_1 = DogForm()                                                      # On créé un formulaire basé sur forms.DogForm et on initialise le paramètre required de tous les fields ( sauf commentaries ) à True ( conséquence, les fields du premier formulaire seront obligatoire !!! )

        for field in fields:
            if field != 'commentaries':
                dog_1.fields[field].required = True

        dog_2 = DogForm()                                                      # Puis on va succéssivement créer 4 autres forms basés sur forms.DogForm en mettant à jour les id de leurs fields à chaque fois ( on va se servir de ces id dans le template pour pouvoir set leurs paramètres required à True si le formulaire est display, et False s'il est hide !!! )
        dog_3 = DogForm()
        dog_4 = DogForm()
        dog_5 = DogForm()

        forms = [dog_2, dog_3, dog_4, dog_5]

        for form in forms:
            for field in fields:
                form.fields[field].widget.attrs['id'] = field+"_dog"+str(i)
                print(form.fields[field].widget.attrs['id'])
            i+=1
        

    return render(request, 'administration/reservation_form.html', {'park_and_client': park_and_client, 'dog_1': dog_1, 'dog_2': dog_2, 'dog_3': dog_3, 'dog_4': dog_4, 'dog_5': dog_5})

@user_passes_test(lambda u: u.is_superuser)
def arrival_and_departure_interface(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        year = request.POST.get('year')
        month = request.POST.get('month')
        # check whether it's valid:
        if year and month:
            # process the data in form.cleaned_data as required
            print(year, month)
            return HttpResponseRedirect('/arrival-departure_interface/')

    # if a GET (or any other method) we'll create a blank form
    else:
        time_frame = SelectTimeFrameForm()
    return render(request, 'administration/arrival-departure_interface.html', {'time_frame': time_frame})
