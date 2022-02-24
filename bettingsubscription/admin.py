from django.contrib import admin
from .models import BettingMembership, BettingUserMembership, BettingSubscription, BettingPayHistory, BetForcast

admin.site.register(BettingUserMembership)
admin.site.register(BettingMembership)
admin.site.register(BettingSubscription)
admin.site.register(BettingPayHistory)
admin.site.register(BetForcast)

