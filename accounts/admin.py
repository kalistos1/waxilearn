from django.contrib import admin
from .models import Notification, Profile, User # Payments

# Register your models here.

admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(User)
#admin.site.register(Payments)
