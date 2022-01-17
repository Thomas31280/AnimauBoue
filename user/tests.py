from django.test import TestCase, Client
import datetime

from django.contrib.auth.models import User
from administration.models import Clients, Dogs, Parks, Reservations

############################
#########Unit Tests#########
############################

class UserTests(TestCase):
    
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

        Reservations.objects.create(client=self.client_1, park=self.park_1, price=140, dog_1=self.dog_1, dog_1_arrival=datetime.datetime(2022, 1, 10), dog_1_departure=datetime.datetime(2022, 2, 10), dog_2=None, dog_2_arrival=None, dog_2_departure=None, dog_3=None, dog_3_arrival=None, dog_3_departure=None, dog_4=None, dog_4_arrival=None, dog_4_departure=None, dog_5=None, dog_5_arrival=None, dog_5_departure=None)
        self.reservation_1 = Reservations.objects.get(price=140)

    # test that a get request on ConsultAvailability returns a 200
    def test_ConsultAvailability_get(self):
        c = Client()
        c.login(username='user', password='password')

        response = c.get('/consult_availability/')
        self.assertEqual(response.status_code, 200)

    # test that a get request on ConnectAdminSpace returns a 200
    def test_ConsultAvailability_post(self):
        c = Client()
        c.login(username='user', password='password')

        datas = {'month': 1, 'year': 2022}

        response = c.post('/consult_availability/', datas)
        self.assertEqual(response.status_code, 200)
