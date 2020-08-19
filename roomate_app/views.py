from django.shortcuts import render, redirect
from .models import Apartment, MyUser, Chore
from django.contrib.auth.models import User
from .forms import ApartmentForm

# Create your views here.
def index(request):
    return render(request, 'roomate_app/index.html')

def dashboard(request):
    #check if the user has an apartment or not
    return render(request, 'roomate_app/dummy.html')
#Create a new apartment.
def new_apt(request):
    if request.method != 'POST':
        #need to raise a flash here (NOT IMPLEMENTED)
        return redirect('roomate_app:dashboard')
    my_apartment = Apartment()
    my_apartment.save()
    current_user = request.user
    current_user.myuser.myApt = my_apartment
    current_user.myuser.save()
    return redirect('roomate_app:dashboard')

#Get an existing apartment.
def assign_apt(request):
    current_user = request.user
    if request.method != 'POST':
        form = ApartmentForm()
    else:
        form = ApartmentForm(data=request.POST)
        if form.is_valid():
            input_token = form.fields[0]
            current_user.myuser.myApt = Apartment.objects.get(token=input_token)
            current_user.save()
            return redirect('roomate_ap:dashboard')
    context = {'form': form}
    return render(request, 'roomate_app/join_apartment.html', context)

