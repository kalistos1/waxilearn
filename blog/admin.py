from django.contrib import admin
from .models import BlogCategory, BlogComments,Post
# Register your models here.


admin.site.register(BlogCategory)
admin.site.register(BlogComments)
admin.site.register(Post)