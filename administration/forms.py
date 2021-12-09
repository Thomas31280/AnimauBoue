from django import forms
from phonenumber_field.formfields import PhoneNumberField

class ConnectionForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'eMail', 'class': 'form-control'}), label="")
    userName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Identifiant', 'class': 'form-control'}), label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control'}), label="")

class UpdateDataForm(forms.Form):
    new_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Nouvel eMail', 'class': 'form-control'}), label="")
    new_userName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nouvel identifiant', 'class': 'form-control'}), label="")
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nouveau mot de passe', 'class': 'form-control'}), label="")
    new_password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez votre nouveau mot de passe', 'class': 'form-control'}), label="")

class AddClientForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'ex : johndoe@protonmail.ru', 'class': 'form-control'}), label="eMail", required=False)
    firstName = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ex : John', 'class': 'form-control'}), label="Prénom")
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ex : Doe', 'class': 'form-control'}), label="Nom")
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'ex : +336XxXxXxXx', 'class': 'form-control'}), label="Coordonées")

class SelectParkAndClientForm(forms.Form):
    OPTIONS = (("", ""), ("1", "E1"), ("2", "E2"),
               ("3", "E3"), ("4", "E4"), ("5", "E5"),
               ("6", "E6"), ("7", "E7"), ("8", "E8"),
               ("9", "E9"), ("10", "E10"))

    park = forms.ChoiceField(widget=forms.Select(attrs={'id': 'park', 'style': "width: 100px;"}), choices=OPTIONS, label="Sélectionnez un parc :")
    client_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'client_id'}))

class DogForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ex : Medor', 'class': 'form-control','id': '' }), label="Nom du chien :", required=False)
    commentaries = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ex : Toiletter en fin de séjour', 'class': 'form-control', 'id': ''}), label="Commentaires :", required=False)
    arrival_date = forms.DateTimeField(label='Arrivée :', required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'min': "2022-01-01T00:00", 'max': "2060-12-31T23:59", 'id': ''}))
    departure_date = forms.DateTimeField(label='Départ :', required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'min': "2022-01-01T00:00", 'max': "2060-12-31T23:59", 'id': ''}))
