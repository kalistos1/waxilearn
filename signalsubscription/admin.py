from django.contrib import admin
from .models import SignalMembership, SignalUserMembership, SignalSubscription,SignalPayHistory,CryptoSignal

admin.site.register(SignalUserMembership)
admin.site.register(SignalMembership)
admin.site.register(SignalSubscription)
admin.site.register(SignalPayHistory)
admin.site.register(CryptoSignal)


