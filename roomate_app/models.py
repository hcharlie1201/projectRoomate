from django.db import models

# Create your models here.

class Apartment(models.Model):
    apt_id = models.AutoField(primary_key=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta: 
        verbose_name_plural = "apartments"

    def __str__(self):
        return "Apartment " + str(self.apt_id)


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    myApt = models.ForeignKey(Apartment, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "users"

    def __str__(self):
        return self.name
