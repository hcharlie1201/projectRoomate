from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from roomate_app.models import Apartment, MyUser, Chore
from roomate_app.views import new_apt, assign_apt, new_chore

class AddChoreTests(TestCase):
    def setUp(self):
        self.apartment = Apartment.objects.create()

        self.auth_user1 = User.objects.create(username='user1')
        self.auth_user1.set_password('abc123456789')
        self.auth_user1.myuser.myApt = self.apartment
        self.auth_user1.save()

    def test_add_chore(self):
        self.client.login(username='user1', password='abc123456789')
        _ = self.client.post('/newchore/', {'name':'Wash dishes', 'description':'Wash dishes'})
        a_chore = Chore.objects.get(pk=1)
        self.assertIsNotNone(a_chore)
        self.assertEqual(a_chore.name, 'Wash dishes')
        self.assertEqual(a_chore.description, 'Wash dishes')
        self.assertEqual(a_chore.creator, self.auth_user1)
    