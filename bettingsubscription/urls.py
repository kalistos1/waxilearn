from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^subscribe/', views.Betting_subscribe, name='betting_subscribe'),
    url(r'^subscribed/', views.Betting_subscribed, name='betting_subscribed'),
    url(r'^sub/', views.Betting_end_sub, name='betting_end_sub'),
    url(r'^payment/$', views.Betting_call_back_url, name='signal_payment'),
    path('create_forecast/', views.CreateForecast, name='create_forecast'),
    path('edit_forecast/<int:pk>/', views.EditForecast, name='edit_forecast'),
    path('delete_forecast/<int:pk>/', views.DeleteForecast, name='delete_forecast'),
    path('preview_forecast/<int:pk>/', views.PreviewForecast, name='preview_forecast'),
    path('all_forecast/', views.AllForecast, name='all_forecast'),
    path('all_subscribers_forecast/', views.subscriberAllForecast, name='all_subscriber_forecast'),
    path('student_view_forecast/<int:pk>/', views.subscriberViewForecast, name='student_view_forecast'),
    path('create/subscription_type/bet_forecast/', views.Instructor_create_sports_sub, name='create_forecast_sub'),
 
]