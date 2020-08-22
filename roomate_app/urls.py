from django.urls import path

from . import views

app_name = 'roomate_app'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('newapt/', views.new_apt, name='newApartment'),
    path('joinapt/', views.assign_apt, name='joinApartment'),
    path('newchore/', views.new_chore, name='newChore')
]