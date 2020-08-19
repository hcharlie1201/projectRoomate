from django import forms

from .models import MyUser, Apartment, Chore

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['text']
        lables = {'text': ''}