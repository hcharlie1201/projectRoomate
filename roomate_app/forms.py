from django import forms
from django.contrib.auth.models import User
from .models import MyUser, Apartment, Chore

class JoinApartmentForm(forms.Form):
    apt_token = forms.CharField()

class CreateChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ['name', 'description', 'assignees']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateChoreForm, self).__init__(*args, **kwargs)

        my_user = self.user.myuser
        myusers = MyUser.objects.filter(myApt=my_user.myApt)
        self.fields['assignees'].queryset = User.objects.filter(myuser__in=myusers)
        #users = []
        #myUsers = MyUser.objects.filter(myApt=self.user.myuser.myApt)
        #for myUser in myUsers:
        #    if self.user.username != myUser.user.username:
        #        users.append((self.user, myUser.user))

