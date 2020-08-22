from django import forms

from .models import MyUser, Apartment, Chore

class JoinApartmentForm(forms.Form):
    apt_token = forms.CharField()

class CreateChoreForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=500)
