from django.conf.urls import url
from django.urls import path
from . import views




urlpatterns = [
    url(r'^subscribe/', views.Signal_subscribe, name='signal_subscribe'),
    url(r'^subscribed/', views.Signal_subscribed, name='signal_subscribed'),
    url(r'^sub/', views.Signal_end_sub, name='signal_sub'),
    url(r'^payment/$', views.Signal_call_back_url, name='signal_payment'),
    path('create/', views.CreateSignals, name='create_signals'),
    path('edit_signal/<int:pk>/', views.EditSignal, name='edit_signal'),
    path('delete_signal/<int:pk>/', views.DeleteSignal, name='delete_signal'),
    path('preview_signal/<int:pk>/', views.previewSignal, name='preview_signal'),
    path('all_signal/', views.all_signal, name='all_signal'),
    path('all_subscriber_signals',views.studentAllSignal, name='student_all_signal'),
    path('subscriber_view_signals/<int:pk>/',views.studentViewSignal, name='student_view_signal'),
    path('create/subscription_type/signals/',views.Instructor_create_signal_sub, name='create_signals_sub'),
    
]