from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from roomate_app.models import Apartment, MyUser, Chore

class CompleteChoreTest(TestCase):
    def setUp(self):
        self.apartment = Apartment.objects.create()

        self.auth_user1 = User.objects.create(username='user1')
        self.auth_user1.set_password('abc123456789')
        self.auth_user1.myuser.myApt = self.apartment
        self.auth_user1.save()

        Chore.objects.create(apt_id=self.apartment, name="Clean kitchen",
                             creator=self.auth_user1)
        Chore.objects.create(apt_id=self.apartment, name="Wash dishes",
                             creator=self.auth_user1)

    def test_add_chore(self):
        self.client.login(username='user1', password='abc123456789')
        _ = self.client.post('/complete/1/', {})
        all_chores = Chore.objects.all()
        self.assertEqual(len(all_chores), 1)
        self.assertRaises(Chore.DoesNotExist, Chore.objects.get, pk=1)
    