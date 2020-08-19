from django.test import TestCase
from django.contrib.auth.models import User
from roomate_app.models import Apartment, MyUser
from roomate_app.views import new_apt, assign_apt

class AptTests(TestCase):
    def setUp(self):
        self.auth_user1 = User.objects.create(username='user1')
        self.auth_user1.set_password('abc123456789')
        self.auth_user2 = User.objects.create(username='user2')
        self.auth_user2.set_password('abc123456789')
        self.auth_user1.save()
        self.auth_user2.save()

        self.dummy_apartment = Apartment.objects.create()

        self.dummy_user1 = MyUser()
        self.dummy_user2 = MyUser()

        self.dummy_user1.user_id = self.auth_user1.id
        self.dummy_user2.user_id = self.auth_user2.id
        self.dummy_user1.save()
        self.dummy_user2.save()

    def test_new_apartment(self):
        self.client.login(username='user1', password='abc123456789')
        _ = self.client.post('/newapt/', {})
        self.assertIsNotNone(self.auth_user1.myuser.myApt)
    
    def test_join_apartment(self):
        self.client.login(username='user2', password='abc123456789')
        _ = self.client.post('/joinapt/', {'apt_token':self.dummy_apartment.token})
        self.assertIsNotNone(self.auth_user2.myuser.myApt)

    def test_new_apartment_sad(self):
        pass
