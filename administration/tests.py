from django.test import TestCase, Client
from django.urls import reverse
import datetime

from django.contrib.auth.models import User
from administration.models import Clients, Dogs, Parks, Reservations

############################
#########Unit Tests#########
############################

class AdministrationTests(TestCase):
    
    def setUp(self):
        User.objects.create_superuser('user', 'user@mail.com', 'password').save()
        
        Parks.objects.create(name='E1', availability=True).save()
        Parks.objects.create(name='E2', availability=True).save()
        Parks.objects.create(name='E3', availability=True).save()
        self.park_1 = Parks.objects.get(name='E1')
        self.park_2 = Parks.objects.get(name='E2')
        self.park_3 = Parks.objects.get(name='E3')
        
        Clients.objects.create(first_name='first_name_1', name='name_1', phone='+33602157836').save()
        Clients.objects.create(first_name='first_name_2', name='name_2', phone='+33602157837').save()
        Clients.objects.create(first_name='first_name_3', name='name_3', phone='+33602157838').save()
        self.client_1 = Clients.objects.get(first_name='first_name_1')
        self.client_2 = Clients.objects.get(first_name='first_name_2')
        self.client_3 = Clients.objects.get(first_name='first_name_3')

        Dogs.objects.create(name='name_1', owner=self.client_1).save()
        Dogs.objects.create(name='name_2', owner=self.client_2).save()
        Dogs.objects.create(name='name_3', owner=self.client_3).save()
        self.dog_1 = Dogs.objects.get(name='name_1')
        self.dog_2 = Dogs.objects.get(name='name_2')
        self.dog_3 = Dogs.objects.get(name='name_3')

        Reservations.objects.create(client=self.client_1, park=self.park_1, price=140, dog_1=self.dog_1, dog_1_arrival=datetime.datetime(2022, 1, 10, 12, 15), dog_1_departure=datetime.datetime(2022, 2, 10, 12, 15), dog_2=None, dog_2_arrival=None, dog_2_departure=None, dog_3=None, dog_3_arrival=None, dog_3_departure=None, dog_4=None, dog_4_arrival=None, dog_4_departure=None, dog_5=None, dog_5_arrival=None, dog_5_departure=None)
        self.reservation_1 = Reservations.objects.get(price=140)

    # test that index returns a 200
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    # test that a get request on ConnectAdminSpace returns a 200
    def test_ConnectAdminSpace_get(self):
        response = self.client.get(reverse('connect_admin_space'))
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on ConnectAdminSpace returns a 302
    def test_ConnectAdminSpace_post(self):
        username = 'user'
        email = 'user@mail.com'
        password = 'password'
        
        post_data = {"userName": username, "password": password, 'email': email}

        response = self.client.post(reverse('connect_admin_space'), data=post_data)
        self.assertEqual(response.status_code, 302)

    # test that a get request on UpdateProfile returns a 200
    def test_UpdateProfile_get(self):
        c = Client()
        c.login(username='user', password='password')
        response = c.get('/update_profile/')
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on UpdateProfile returns a 302
    def test_UpdateProfile_post(self):
        c = Client()
        c.login(username='user', password='password')
        username = 'user'
        email = 'user@mail.com'
        password = 'password'
        new_password = 'new_password'
        new_password_confirm = new_password
        new_username = 'new_user'
        new_email = 'new_user@mail.com'
        
        post_data = {"userName": username, "password": password, "email": email,
                     "new_password": new_password, "new_password_confirm": new_password_confirm,
                     "new_username": new_username, "new_email": new_email}

        response = c.post("/update_profile/", data=post_data)
        self.assertEqual(response.status_code, 302)

    # test that a get request on administration_interface returns a 200
    def test_administration_interface(self):
        c = Client()
        c.login(username='user', password='password')
        response = c.get('/administration_interface/')
        self.assertEqual(response.status_code, 200)
    
    # test that a get request on user_logout returns a 302
    def test_logout(self):
        c = Client()
        c.login(username='user', password='password')
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 302)
    
    # test that a get request on ParksAvalability returns a 200
    def test_ParksAvailability_get(self):
        c = Client()
        c.login(username='user', password='password')
        response = c.get('/parks_availability/')
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on ParksAvalability returns a 302
    def test_ParksAvailability_post(self):
        c = Client()
        c.login(username='user', password='password')
        park_to_update = Parks.objects.get(name='E1').id
        
        post_data = {"park": park_to_update}

        response = c.post("/parks_availability/", data=post_data)
        self.assertEqual(response.status_code, 302)

    # test that a get request on AddClient returns a 200
    def test_AddClient_get(self):
        c = Client()
        c.login(username='user', password='password')
        response = c.get('/add_client_form/')
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on AddClient returns a 302
    def test_AddClient_post(self):
        c = Client()
        c.login(username='user', password='password')
        
        datas = {'firstName': 'first_name', 'name': 'name', 'phone': '+33613008748', 'email': ''}

        response = c.post('/add_client_form/', datas)
        self.assertEqual(response.status_code, 302)
    
    # test that a get request on AddClient returns a 200
    def test_UpdateClient_get(self):
        c = Client()
        c.login(username='user', password='password')
        
        datas = {'client': self.client_1.id, 'client_phone': str(self.client_1.phone)}

        response = c.get('/update_client/', datas)
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on AddClient returns a 302
    def test_UpdateClient_post(self):
        c = Client()
        c.login(username='user', password='password')
        
        datas = {'firstName': 'first_name', 'phone': '+33613008748', 'email': '', 'client_id': self.client_1.id, 'current_phone': self.client_1.phone}

        response = c.post('/update_client/', datas)
        self.assertEqual(response.status_code, 302)
    
    # test that a get request on client_reservations returns a 200
    def test_client_reservations(self):
        c = Client()
        c.login(username='user', password='password')
        
        datas = {'client': self.client_1.id, 'client_phone': str(self.client_1.phone)}

        response = c.get('/client_reservations/', datas)
        self.assertEqual(response.status_code, 200)

    # test that a post request on delete_client returns a 302
    def test_delete_client(self):
        c = Client()
        c.login(username='user', password='password')
        
        datas = {'client_id': self.client_1.id, 'client_phone': str(self.client_1.phone)}

        response = c.post('/delete_client/', datas)
        self.assertEqual(response.status_code, 302)

    # test that a post request on clients_profiles returns a 200
    def test_clients_profiles(self):
        c = Client()
        c.login(username='user', password='password')
        
        datas = {'recherche_client': 'name'}

        response = c.post('/clients_profiles_client/', datas)
        self.assertEqual(response.status_code, 200)
    
    # test that a get request on delete_client returns a 302
    def test_delete_client(self):
        c = Client()
        c.login(username='user', password='password')

        response = c.post('/delete_client/', {'client_id': self.client_2.id, 'client_phone': str(self.client_2.phone)})
        self.assertEqual(response.status_code, 302)
    
    # test that a get request on client returns a 200
    def test_client(self):
        c = Client()
        c.login(username='user', password='password')

        response = c.get('/client/', {'client': self.client_1.id})
        self.assertEqual(response.status_code, 200)
    
    # test that a get request on client returns a 302 if client doesn't exist
    def test_client_fail(self):
        c = Client()
        c.login(username='user', password='password')

        response = c.get('/client/', {'client': ''})
        self.assertEqual(response.status_code, 302)
    
    # test that a get request on ReservationForm returns a 200
    def test_ReservationForm_get(self):
        c = Client()
        c.login(username='user', password='password')

        response = c.get('/reservation_form/')
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on ReservationForm returns a 200
    def test_ReservationForm_post(self):
        c = Client()
        c.login(username='user', password='password')

        response = c.post('/reservation_form/', {'recherche_client': 'name'})
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on delete_reservation returns a 302
    def test_delete_reservation_post(self):
        c = Client()
        c.login(username='user', password='password')

        datas = {'reservation_id': self.reservation_1.id, 'client': self.reservation_1.client.id}

        response = c.post('/delete_reservation/', datas)
        self.assertEqual(response.status_code, 302)

    # test that a get request on ArrivalAndDeparture returns a 200
    def test_ArrivalAndDeparture_get(self):
        c = Client()
        c.login(username='user', password='password')

        response = c.get('/arrival-departure_interface/')
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on ArrivalAndDeparture returns a 200
    def test_ArrivalAndDeparture_post(self):
        c = Client()
        c.login(username='user', password='password')

        datas = {'month': 1, 'year': 2022}

        response = c.post('/arrival-departure_interface/', datas)
        self.assertEqual(response.status_code, 200)
    
    # test that a get request on Stats returns a 200
    def test_Stats_get(self):
        c = Client()
        c.login(username='user', password='password')

        response = c.get('/stats/')
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on Stats returns a 200
    def test_Stats_post(self):
        c = Client()
        c.login(username='user', password='password')

        datas = {'month': 1, 'year': 2022}

        response = c.post('/stats/', datas)
        self.assertEqual(response.status_code, 200)
    
    # test that a get request on NewDog returns a 200
    def test_NewDog_get(self):
        c = Client()
        c.login(username='user', password='password')

        response = c.get('/add_dog/', {'client': self.client_1.id, 'client_phone': str(self.client_1.phone)})
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on NewDog returns a 302
    def test_NewDog_post(self):
        c = Client()
        c.login(username='user', password='password')

        datas = {'client_id': self.client_1.id, 'client_phone': str(self.client_1.phone), 'name': 'name', 'transponder': 874521201254862}

        response = c.post('/add_dog/', datas)
        self.assertEqual(response.status_code, 302)
    
    # test that a post request on NewDog returns a 302 if bad transponder
    def test_NewDog_bad_transponder(self):
        c = Client()
        c.login(username='user', password='password')

        datas = {'client_id': self.client_1.id, 'client_phone': str(self.client_1.phone), 'name': 'name', 'transponder': '874521201254862'}

        response = c.post('/add_dog/', datas)
        self.assertEqual(response.status_code, 302)
    
    # test that a post request on NewDog returns a 302 if client.phone != client_phone
    def test_NewDog_bad_client_phone(self):
        c = Client()
        c.login(username='user', password='password')

        datas = {'client_id': self.client_1.id, 'client_phone': str(self.client_2.phone), 'name': 'name', 'transponder': 874521201254862}

        response = c.post('/add_dog/', datas)
        self.assertEqual(response.status_code, 302)
    
    # test that a get request on UpdateDog returns a 200
    def test_UpdateDog_get(self):
        c = Client()
        c.login(username='user', password='password')

        response = c.get('/update_dog/', {'dog': self.dog_1.id, 'owner': self.dog_1.owner.id})
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on UpdateDog returns a 302
    def test_UpdateDog_post(self):
        c = Client()
        c.login(username='user', password='password')

        datas = {'dog_id': self.dog_1.id, 'owner_id': self.dog_1.owner.id, 'name': 'new_name', 'transponder': 874521521754862}

        response = c.post('/update_dog/', datas)
        self.assertEqual(response.status_code, 302)
    
    # test that a post request on delete_dog returns a 302
    def test_delete_dog_post(self):
        c = Client()
        c.login(username='user', password='password')

        datas = {'dog_id': self.dog_1.id, 'owner': self.dog_1.owner.id}

        response = c.post('/delete_dog/', datas)
        self.assertEqual(response.status_code, 302)

    # test that a get request on UpdateReservation returns a 200
    def test_UpdateReservation_get(self):
        c = Client()
        c.login(username='user', password='password')

        response = c.get('/update_reservation/', {'reservation': self.reservation_1.id, 'client_phone': str(self.reservation_1.client.phone)})
        self.assertEqual(response.status_code, 200)