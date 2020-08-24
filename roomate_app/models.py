from django.db import models
from django.contrib.auth.models import User
import json
import secrets
from django.db.models.signals import post_save
from django.dispatch import receiver
from hashlib import sha1
# Create your models here.


class Apartment(models.Model):
    apt_id = models.AutoField(primary_key=True)
    date_added = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=100, default=sha1((secrets.token_urlsafe() + str(apt_id)).encode('utf-8')).hexdigest())

    class Meta:
        verbose_name_plural = "apartments"

    def __str__(self):
        return "Apartment " + str(self.apt_id)


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    myApt = models.ForeignKey(Apartment, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "myusers"


@receiver(post_save, sender=User)
def create_user_myuser(sender, instance, created, **kwargs):
    if created:
        MyUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_myuser(sender, instance, **kwargs):
    instance.myuser.save()


class Chore(models.Model):
    apt_id = models.ForeignKey(Apartment, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
<<<<<<< HEAD
    creator = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='creator_user')
    assignees = models.ManyToManyField(User, blank=True)
=======
    creator = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE, related_name='creator_user')
    assignees = models.ManyToManyField(User, blank=True, default="")
>>>>>>> 38aed040e8be2eb7579d9daf3387c0b56fc5e874
    description = models.CharField(max_length=500, default="Description of Chore")
    complete = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def set_assignees(self, nameList):
        self.assignees = json.dumps(nameList)

    def get_assignees(self):
        return json.loads(self.assignees)

    class Meta:
        verbose_name_plural = "chores"

    def __str__(self):
        return self.name
