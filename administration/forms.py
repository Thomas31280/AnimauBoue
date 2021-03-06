from django import forms
from phonenumber_field.formfields import PhoneNumberField
from administration.models import Parks


class ConnectionForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'eMail', 'class': 'form-control'}), label="")
    userName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Identifiant', 'class': 'form-control'}), label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control'}), label="")


class UpdateDataForm(forms.Form):
    new_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Nouvel eMail', 'class': 'form-control'}), label="")
    new_username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nouvel identifiant', 'class': 'form-control'}), label="")
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nouveau mot de passe', 'class': 'form-control'}), label="")
    new_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez votre nouveau mot de passe', 'class': 'form-control'}), label="")


class AddClientForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'ex : johndoe@protonmail.ru', 'class': 'form-control'}), label="eMail", required=False, max_length=65)
    firstName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ex : John', 'class': 'form-control'}), label="Prénom", max_length=30)
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ex : Doe', 'class': 'form-control'}), label="Nom", max_length=30)
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'ex : +336XxXxXxXx', 'class': 'form-control'}), label="Coordonées")


class SelectParkAndClientForm(forms.Form):
    parks = Parks.objects.filter(availability=True).order_by('id')
    OPTIONS = [("", "")]

    # Les parcs proposés dans les formulaires ne doivent être que ceux qui sont disponnibles. De plus, les id doivent être valables, donc il vaut mieux créer ce form avec une itération sur les instances de la table Parks
    for park in parks:
        OPTIONS.append((str(park.id), str(park.name)))
    OPTIONS = tuple(OPTIONS)

    park = forms.ChoiceField(widget=forms.Select(attrs={'id': 'park', 'style': "width: 100px;"}), choices=OPTIONS, label="Sélectionnez un parc :")
    client_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'client_id'}))


class DogForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ex : Medor', 'class': 'form-control', 'id': ''}), label="Nom du chien :", required=False)
    arrival_date = forms.DateTimeField(label='Arrivée :', required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'min': "2022-01-01T00:00", 'max': "2060-12-31T23:59", 'id': ''}))
    departure_date = forms.DateTimeField(label='Départ :', required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'min': "2022-01-01T00:00", 'max': "2060-12-31T23:59", 'id': ''}))
    prefix = 'form1'


class SelectTimeFrameForm(forms.Form):
    MONTHS = (("", ""), (1, "Janvier"), (2, "Février"),
              (3, "Mars"), (4, "Avril"), (5, "Mai"),
              (6, "Juin"), (7, "Juillet"), (8, "Août"),
              (9, "Septembre"), (10, "Octobre"), (11, "Novembre"),
              (12, "Décembre"))
    YEARS = [("", "")]

    for year in range(2022, 2061):
        YEARS.append((year, str(year)))
    YEARS = tuple(YEARS)

    month = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width: 100px;', 'class': 'margin-left: 50%;', 'id': 'month'}), choices=MONTHS, label="Mois :")
    year = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width: 80px;', 'class': 'margin-left: 50%;', 'id': 'year'}), choices=YEARS, label="Année :")


class AddDog(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ex : Séraphin', 'class': 'form-control'}), label="Nouveau chien :", max_length=30)
    transponder = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Format : 15 chiffres', 'class': 'form-control'}), required=False, label="Numéro de transpondeur :")
