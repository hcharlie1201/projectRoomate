from django.urls import path

from . import views

app_name = 'roomate_app'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
]