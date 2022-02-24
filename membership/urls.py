from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^subscription/', views.subscription, name='subscription'),
    url(r'^subscribe/', views.subscribe, name='subscribe'),
    url(r'^subscribed/', views.subscribed, name='subscribed'),
    url(r'^sub/', views.end_sub, name='sub'),
    url(r'^payment/$', views.call_back_url, name='payment'),
    url(r'^create/subscription_type/students/', views.Instructor_create_student_sub, name='create_student_sub'),
]