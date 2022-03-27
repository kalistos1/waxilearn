from django.urls import path
from .import views

urlpatterns = [
    path('', views.PostList, name="postlist"),
    path('posts/<slug>/read', views.PostDetail, name="postdetail"),
     path('posts/category/<slug>', views.category_post_list, name="postcat"),
    path('admin/post/add_post/',views.create_post, name="create_post"),
    path('admin/posts/view/all/',views.admin_all_blog_post, name="admin_all_post"),
    path('admin/post/edit/<slug>/',views.edit_post, name="edit_post"),
    path('admin/post/delete/<slug>/',views.delete_post, name="delete_post"),
]