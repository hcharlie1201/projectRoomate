from django.contrib import admin

# Register your models here.
from .models import MyUser, Apartment, Chore

admin.site.register(MyUser)
admin.site.register(Apartment)
admin.site.register(Chore)
