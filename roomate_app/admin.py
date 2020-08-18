from django.contrib import admin

# Register your models here.
from .models import User, Apartment, Chore

admin.site.register(User)
admin.site.register(Apartment)
admin.site.register(Chore)