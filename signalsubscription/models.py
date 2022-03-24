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
class SignalPayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    paystack_charge_id = models.CharField(max_length=100, default='', blank=True)
    paystack_access_code = models.CharField(max_length=100, default='', blank=True)
    payment_for = models.ForeignKey('SignalMembership', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

#### Membership
class SignalMembership(models.Model):
    MEMBERSHIP_CHOICES = (
    	#('Extended', 'Extended'), # Note that they are all capitalize//
    	#('Advanced', 'Advanced'),
    	('Gold', 'Gold'),
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
class SignalUserMembership(models.Model):
    user = models.OneToOneField(User, related_name='signal_user_membership', on_delete=models.CASCADE)
    signal_membership = models.ForeignKey(SignalMembership, related_name='signal_user_membership', on_delete=models.SET_NULL, null=True)
    reference_code = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
       return self.user.username

@receiver(post_save, sender=SignalUserMembership)
def create_subscription(sender, instance, *args, **kwargs):
	if instance:
		SignalSubscription.objects.create(signal_user_membership=instance, expires_in=dt.now().date() + timedelta(days=instance.signal_membership.duration))


#### User Subscription
class SignalSubscription(models.Model):
    signal_user_membership = models.ForeignKey(SignalUserMembership, related_name='signalsubscription', on_delete=models.CASCADE, default=None)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
      return self.signal_user_membership.user.username

@receiver(post_save, sender=SignalSubscription)
def update_active(sender, instance, *args, **kwargs):
	if instance.expires_in < today:
		signalsubscription = SignalSubscription.objects.get(id=instance.id)
		signalsubscription.delete()


class CryptoSignal(models.Model):
    signal_id = models.CharField(max_length=50, editable=False)
    instructor = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(null=False, blank=False, max_length=100)
    photo = models.ImageField(null=True, upload_to='signals/')
    description =models.CharField(null=False, blank=False, max_length=200)
    body = RichTextField()
    created_on = models.DateField(editable=False, auto_now_add=True)
    last_modified = models.DateField(editable=False, auto_now=True)

    def __str__(self):
        return self.title

    