from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from roomate_app.models import MyUser 
from django.contrib import messages
from . import forms
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = forms.RegisterUserForm(data=request.POST)

        if form.is_valid():
            auth_user = form.save()

            my_user = MyUser()
            my_user.user_id = auth_user.id
            my_user.save()

            login(request, auth_user)
            return redirect('roomate_app:dashboard')

    form = forms.RegisterUserForm()
    messages.warning(request, 'Failed To Create A Profile. Please Try Again.')
    return render(request, 'register.html', {'form':form})
