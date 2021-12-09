from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import ConnectionForm, UpdateDataForm, AddClientForm, SelectParkAndClientForm, DogForm

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
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ConnectionForm()

    return render(request, 'administration/admin_connect_space.html', {'form': form})

def update_profile_interface(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        current_datas = ConnectionForm(request.POST)
        new_datas = UpdateDataForm(request.POST)
        # check whether it's valid:
        if current_datas.is_valid() and new_datas.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

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
    template = loader.get_template('administration/clients.html')
    return HttpResponse(template.render(request=request))

def add_client_form(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        add_client_form = AddClientForm(request.POST)
        # check whether it's valid:
        if add_client_form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

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

def arrival_and_departure_interface(request):
    template = loader.get_template('administration/arrival-departure_interface.html')
    return HttpResponse(template.render(request=request))
