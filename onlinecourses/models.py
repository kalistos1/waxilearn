
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from accounts.models import User
from embed_video.fields import EmbedVideoField
import random
from ckeditor.fields import RichTextField 
# Create your models here.


# Create your models here.
class Category(models.Model):
    category_id = models.CharField(max_length=50, )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=350)

    class Meta:
        verbose_name_plural = 'categories'
        db_table = 'categories'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):        
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)



class Course(models.Model):
    course_id = models.CharField(max_length=50, editable=False)
    title = models.CharField(max_length=350)
    slug = models.SlugField(max_length=450)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    description = RichTextField()
    objective = RichTextField()
    eligibility = RichTextField()
    instructor = models.ForeignKey(User, on_delete = models.CASCADE)
    photo = models.ImageField(null=True, upload_to='courses/photos/')
    created_on = models.DateField(editable=False, auto_now_add=True)
    last_modified = models.DateField(editable=False, auto_now=True)

    def save(self, *args, **kwargs):
        self.course_id = "CC" + str(random.randint(1000000, 90000000))
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super(Course, self).save(*args, **kwargs)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    lesson_id = models.CharField(max_length=50, editable=False)
    title = models.CharField(max_length=450)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    add_video = EmbedVideoField(blank=True)
    slug = models.SlugField(max_length=450, editable=False)
    description = RichTextField()

    def save(self, *args, **kwargs):
        self.lesson_id = "LL" + str(random.randint(1000000, 90000000))
        value = self.title
        self.slug = slugify(value, allow_unicode=True)       
        super(Lesson, self).save(*args, **kwargs)


    class Meta:
        db_table = 'lessons'

    def __str__(self):
        return self.title


"""
class Video(models.Model):
    video_id = models.CharField(max_length=50, )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=350)
    duration = models.CharField(max_length=450)
    url = EmbedVideoField(blank=True)
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'videos'

    def __str__(self):
        return self.title
"""

class Text(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=350)
    body   = RichTextField()
    slug   = models.SlugField(unique = True)
    duration = models.CharField(max_length=450, null=True, blank=True)
    created_on = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now= True)

    class Meta:
        db_table = 'text'

    def __str__(self):
        return self.title       
    
class Comment(models.Model):
    comment_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    content = RichTextField()
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'comments'
        unique_together = ('user', 'course')
        

class StudentCourses(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date_purchased = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'student_courses'
        verbose_name_plural = 'student courses'
        unique_together = ('course', 'user')

    def __str__(self):
        return self.course.title + " owned by " + self.user.first_name
