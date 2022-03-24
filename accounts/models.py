from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
#from onlinecourses.models import Course
# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default =False)
    is_student = models.BooleanField('Is student', default =False)
    is_instructor = models.BooleanField('Is Instructor', default =False)
    

class Notification(models.Model):
    text = models.TextField()
    active = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text


    class Meta:
        db_table = 'notifications'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(upload_to='users/', default='user.png',blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)        
    email_confirmed = models.BooleanField(default=False)
    country = models.CharField(max_length=50, null=True, blank=True)    
    twitter_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)    
    is_instructor = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    last_modified = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'profiles'


    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
        
    
"""
class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    created_on = models.DateTimeField(auto_now=True)
"""