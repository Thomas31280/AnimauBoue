from django.test import TestCase, Client
from django.urls import reverse

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
        park_1 = Parks.objects.get(name='E1')
        park_2 = Parks.objects.get(name='E2')
        park_3 = Parks.objects.get(name='E3')
        
        Clients.objects.create(first_name='first_name_1', name='name_1', phone='+33602157836').save()
        Clients.objects.create(first_name='first_name_2', name='name_2', phone='+33602157837').save()
        Clients.objects.create(first_name='first_name_3', name='name_3', phone='+33602157838').save()
        client_1 = Clients.objects.get(first_name='first_name_1')
        client_2 = Clients.objects.get(first_name='first_name_2')
        client_3 = Clients.objects.get(first_name='first_name_3')

        Dogs.objects.create(name='name_1', owner=client_1).save()
        Dogs.objects.create(name='name_2', owner=client_2).save()
        Dogs.objects.create(name='name_3', owner=client_3).save()
        dog_1 = Dogs.objects.get(name='name_1')
        dog_2 = Dogs.objects.get(name='name_2')
        dog_3 = Dogs.objects.get(name='name_3')




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
        Clients.objects.create(first_name='first_name', name='name', phone='+33602157847').save()
        client_id = Clients.objects.get(name='name').id
        
        datas = {'client': client_id, 'client_phone': '+33602157847'}

        response = c.get('/update_client/', datas)
        self.assertEqual(response.status_code, 200)
    
    # test that a post request on AddClient returns a 302
    def test_UpdateClient_post(self):
        c = Client()
        c.login(username='user', password='password')
        client_id = Clients.objects.get(name='name_1').id
        client_phone = Clients.objects.get(name='name_1').phone
        
        datas = {'firstName': 'first_name', 'phone': '+33613008748', 'email': '', 'client_id': client_id, 'current_phone': client_phone}

        response = c.post('/update_client/', datas)
        self.assertEqual(response.status_code, 302)
    
    # test that a get request on client_reservations returns a 200
    def test_client_reservations(self):
        c = Client()
        c.login(username='user', password='password')
        Clients.objects.create(first_name='first_name', name='name', phone='+33602157847').save()
        client_id = Clients.objects.get(name='name').id
        
        datas = {'client': client_id, 'client_phone': '+33602157847'}

        response = c.get('/client_reservations/', datas)
        self.assertEqual(response.status_code, 200)
    
    