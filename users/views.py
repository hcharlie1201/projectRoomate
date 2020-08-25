from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from roomate_app.models import MyUser 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = forms.RegisterUserForm(data=request.POST)

        if form.is_valid():
            auth_user = form.save()
            login(request, auth_user)
            return redirect('roomate_app:dashboard')

    form = forms.RegisterUserForm()
    messages.warning(request, 'Failed To Create A Profile. Please Try Again.')
    return render(request, 'register.html', {'form':form})

@login_required
def change_password(request):

    form = forms.PasswordChangeForm(user=request.user)

    if request.method == 'POST':

        form = forms.PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():

            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('roomate_app:dashboard')

    return render(request, 'registration/change_password.html', {'form':form})

