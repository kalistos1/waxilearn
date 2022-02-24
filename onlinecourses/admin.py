from django.contrib import admin
from . models import Course, Lesson, Text, Category, Comment, StudentCourses


# Register your models here.

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Text)
#admin.site.register(Video)
admin.site.register(Lesson)
admin.site.register(StudentCourses)
admin.site.register(Comment)

