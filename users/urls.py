from django.urls import path, include
from django.contrib.auth import views as views_builtin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from . import forms

app_name = 'users'
urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', CreateView.as_view(template_name='registration/register.html',
        form_class=forms.RegisterUserForm, 
        success_url=reverse_lazy('roomate_app:dashboard')), name='register'),
]
