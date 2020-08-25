from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class ResetPasswordTest(TestCase):
    def setUp(self):
        self.auth_user1 = User.objects.create(username='user1')
        self.auth_user1.set_password('abc123456789')
        self.auth_user1.save()

    def test_add_chore(self):
        self.client.login(username='user1', password='abc123456789')
        _ = self.client.post('/users/change_password/',{'old_password':'abc123456789', 'new_password1':'abc12345678999', 'new_password2':'abc12345678999'})
        new_pass = self.client.login(username='user1', password='abc12345678999')
        old_pass = self.client.login(username='user1', password='abc123456789')
        self.assertTrue(new_pass)
        self.assertFalse(old_pass)
