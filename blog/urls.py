from django.urls import path
from .import views

urlpatterns = [
    path('', views.PostList, name="postlist"),
    path('<slug>', views.PostDetail, name="postdetail")
]