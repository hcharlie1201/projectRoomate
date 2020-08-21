from django.shortcuts import render, redirect
from .models import Apartment, MyUser, Chore
from django.contrib.auth.models import User
from .forms import JoinApartmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'roomate_app/index.html')

@login_required
def dashboard(request):
    #check if the user has an apartment or not
    chores = Chore.objects.filter(apt_id=request.user.myuser.myApt)
    return render(request, 'roomate_app/dashboard.html', {'chores': chores})

#Create a new apartment.
def new_apt(request):
    if request.method != 'POST':
        #need to raise a flash here
        messages.warning(request, 'Failed To Create An Apartment. Please try again.')
        return redirect('roomate_app:dashboard')
    
    my_apartment = Apartment()
    current_user = request.user
    current_user.myuser.myApt = my_apartment
    my_apartment.save()
    current_user.save()
    messages.success(request, 'You Have Successfuly Created A New Apartment!!!')
    return redirect('roomate_app:dashboard')

#Get an existing apartment.
def assign_apt(request):
    current_user = request.user
    if request.method == 'POST':
        form = JoinApartmentForm(request.POST)
        if form.is_valid():
            input_token = form.cleaned_data['apt_token']
            apt_list = Apartment.objects.filter(token=input_token)
            if apt_list.count() > 0:
                current_user.myuser.myApt = Apartment.objects.get(token=input_token)
                current_user.save()
                messages.success(request, 'You Have Successfuly Joined The Apartment!!!')
                return redirect('roomate_app:dashboard')
            else:
                #need to raise a flash here
                messages.error(request, 'Failed to join an Apartment. Please verify your token.')
                form = JoinApartmentForm()
    else:
        form = JoinApartmentForm()

    context = {'form': form}
    return render(request, 'roomate_app/joinApartment.html', context)
    #replate dummy.html with something else
