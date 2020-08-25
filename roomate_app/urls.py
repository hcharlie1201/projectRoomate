from django.urls import path, re_path
from django.conf.urls import url, include


from . import views

app_name = 'roomate_app'
urlpatterns = [ 
    # Home page
    path('', views.index, name='index'),
    url(r'^delete/(?P<chore_id>[0-9]+)/$', views.delete_chore, name='delete_a_chore'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('newapt/', views.new_apt, name='newApartment'),
    path('joinapt/', views.assign_apt, name='joinApartment'),
    path('profile/', views.profile, name='profile'),
    path('newchore/', views.new_chore, name='newChore'),
    path('leaveapt/', views.leave_apt, name='leaveApt'),
    url(r'^complete/(?P<chore_id>[0-9]+)/$', views.complete_chore, name='completeChore'),
]