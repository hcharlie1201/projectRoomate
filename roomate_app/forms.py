from django import forms

from .models import MyUser, Apartment, Chore

class JoinApartmentForm(forms.Form):
    apt_token = forms.CharField()