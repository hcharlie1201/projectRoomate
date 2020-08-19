from django.db import models
from django.contrib.auth.models import User
import json
import secrets

# Create your models here.

class Apartment(models.Model):
    apt_id = models.AutoField(primary_key=True)
    date_added = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=100, default=secrets.token_urlsafe(16))
    
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


class Chore(models.Model):
    name = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    assignees = models.CharField(max_length=500) #optional
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