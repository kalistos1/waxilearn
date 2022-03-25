from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from datetime import date
from datetime import timedelta
from datetime import datetime as dt
from accounts.models import User
from ckeditor.fields import RichTextField 

today = date.today()

# Create your models here.


#### User Payment History
class BettingPayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    paystack_charge_id = models.CharField(max_length=100, default='', blank=True)
    paystack_access_code = models.CharField(max_length=100, default='', blank=True)
    payment_for = models.ForeignKey('BettingMembership', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

#### Membership
class BettingMembership(models.Model):
    MEMBERSHIP_CHOICES = (
    	#('Extended', 'Extended'), # Note that they are all capitalize//
    	#('Advanced', 'Advanced'),
    	('Silver', 'Silver'),
        ('Free', 'Free')
    )
    PERIOD_DURATION = (
        ('Days', 'Days'),
        ('Week', 'Week'),
        ('Months', 'Months'),
    )
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Free', max_length=30)
    duration = models.PositiveIntegerField(default=7)
    duration_period = models.CharField(max_length=100, default='Day', choices=PERIOD_DURATION)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
       return self.membership_type

#### User Membership
class BettingUserMembership(models.Model):
    user = models.OneToOneField(User, related_name='betting_user_membership', on_delete=models.CASCADE)
    betting_membership = models.ForeignKey(BettingMembership, related_name='betting_user_membership', on_delete=models.SET_NULL, null=True)
    reference_code = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
       return self.user.username

@receiver(post_save, sender=BettingUserMembership)
def create_subscription(sender, instance, *args, **kwargs):
	if instance:
		BettingSubscription.objects.create(betting_user_membership=instance, expires_in=dt.now().date() + timedelta(days=instance.betting_membership.duration))


#### User Subscription
class BettingSubscription(models.Model):
    betting_user_membership = models.ForeignKey(BettingUserMembership, related_name='bettingsubscription', on_delete=models.CASCADE, default=None)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
      return self.betting_user_membership.user.username


@receiver(post_save, sender=BettingSubscription)
def update_active(sender, instance, *args, **kwargs):
	if instance.expires_in < today:
		bettingsubscription = BettingSubscription.objects.get(id=instance.id)
		bettingsubscription.delete()


class BetForcast(models.Model):
    Game_status = (
        ('NotStarted', 'NotStarted'),
        ('Ongoing', 'Ongoing'),
        ('Suspended', 'Suspended'),
        ('Ended', 'Ended'),
    )
    forcast_id = models. IntegerField(editable=False)
    instructor = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(null=False, blank=False, max_length=100)
    slug =models.SlugField(null = False, blank = False, unique=True)
    description =models.CharField(null=False, blank=False, max_length=200)
    home_team=models.CharField(null=False, blank=False, max_length=100)
    away_team=models.CharField(null=False, blank=False, max_length=100)
    total_odd = models.CharField(null=False, blank=False, max_length=100)
    start_time = models.TimeField()
    play_status = models.CharField(max_length=100, default='NotStarted', choices=Game_status)
    forcast_win_status = models.BooleanField(default=False)
    created_on = models.DateField(editable=False, auto_now_add=True)
    last_modified = models.DateField(editable=False, auto_now=True)

    def __str__(self):
        return self.title

    
