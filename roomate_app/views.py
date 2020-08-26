from django.shortcuts import render, redirect
from .models import Apartment, MyUser, Chore
from django.contrib.auth.models import User
from .forms import JoinApartmentForm, CreateChoreForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hashlib import sha1
import secrets

# Create your views here.
def index(request):
    if request.user.is_authenticated:  
        return redirect('roomate_app:dashboard')
    return render(request, 'roomate_app/index.html')

@login_required
def dashboard(request):
    #check if the user has an apartment or not
    chores = Chore.objects.filter(apt_id=request.user.myuser.myApt)
    return render(request, 'roomate_app/dashboard.html', {'chores': chores})

#Create a new apartment.
@login_required
def new_apt(request):
    if request.method != 'POST':
        #need to raise a flash here
        messages.warning(request, 'Failed To Create An Apartment. Please try again.')
        return redirect('roomate_app:dashboard')
    
    my_apartment = Apartment.objects.create()
    my_apartment.token = sha1((secrets.token_hex() + str(my_apartment.pk)).encode('utf-8')).hexdigest()
    current_user = request.user
    current_user.myuser.myApt = my_apartment
    my_apartment.save()
    current_user.save()
    return redirect('roomate_app:dashboard')

#Get an existing apartment.
@login_required
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
                return redirect('roomate_app:dashboard')
            else:
                #need to raise a flash here
                messages.warning(request, 'Failed To Join An Apartment. Please Verify Your Token.')
                form = JoinApartmentForm()
    else:
        #need to raise a flash here
        form = JoinApartmentForm()

    context = {'form': form}
    return render(request, 'roomate_app/joinApartment.html', context)

#Create a new chore
@login_required
def new_chore(request):
    current_user = request.user
    apt_id = current_user.myuser.myApt
    if request.method == 'POST':
        form = CreateChoreForm(request.POST, user=current_user)
        if form.is_valid():
            input_name = form.cleaned_data['name']
            input_desc = form.cleaned_data['description']
            input_assignees = form.cleaned_data['assignees']
            new_chore_obj = Chore(apt_id=apt_id, name=input_name, creator=current_user, description=input_desc)
            new_chore_obj.save()
            for assignee in input_assignees:
                new_chore_obj.assignees.add(User.objects.get(username=assignee))
            #messages.success(request, 'You have successfully created a Chore!')
            return redirect('roomate_app:dashboard')
    
    else:
        form = CreateChoreForm(user=current_user)
        
    numUsers = MyUser.objects.filter(myApt=apt_id).count()
    context = {'form': form, 'numUsers': numUsers }
    return render(request, 'roomate_app/newChore.html', context)

@login_required
def delete_chore(request, chore_id =None):
    chore_object = Chore.objects.get(id=chore_id)
    chore_object.delete()
    messages.warning(request, 'Successfully delete.')
    return redirect('roomate_app:dashboard')

@login_required
def profile(request): 
    username = request.user.username
    email = request.user.email
    my_user = request.user.myuser
    apt = my_user.myApt
    apt_token = ""
    if apt == None:
        apt_token = "You are not in an Apartment"
    else:
        apt_token = apt.token
    context = {'username': username, 'email': email, 'apt_token': apt_token}
    return render(request, 'roomate_app/profile.html', context)

@login_required
def leave_apt(request):
    if request.method != 'POST':
        #need to raise a flash here
        messages.warning(request, 'Failed to leave the Apartment. Please try again.')
        return redirect('roomate_app:dashboard')

    current_user = request.user
    apt_id = current_user.myuser.myApt

    my_user = current_user.myuser
    roommates = MyUser.objects.filter(myApt=apt_id)
    if roommates.count() == 1:
        my_user.myApt.delete()

    my_user.myApt = None
    my_user.save()
    return render(request, 'roomate_app/dashboard.html')

@login_required
def complete_chore(request, chore_id=None):
    chore_obj = Chore.objects.get(id=chore_id)
    chore_obj.delete()
    return redirect('roomate_app:dashboard')