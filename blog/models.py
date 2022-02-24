from django.db import models 
from accounts.models import User
from django.utils.text import slugify
from django.utils import timezone
from ckeditor.fields import RichTextField 

# Create your models here.

class BlogCategory(models.Model):
    name = models.CharField(max_length = 250)
    slug = models.SlugField ()
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete = models.CASCADE)

    class Meta:
       unique_together = ('slug', 'parent',)    
       verbose_name_plural = 'blog_categories'
       db_table = 'blog_categories'

    def save(self, *args, **kwargs):        
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super(BlogCategory, self).save(*args, **kwargs)
    
        
    def __str__(self):                           
        full_path = [self.name]                  
        parent_cat = self.parent
        while parent_cat is not None:
            full_path.append(parent_cat.name)
            parent_cat = parent_cat.parent
        return ' -> '.join(full_path[::-1])



#models manager to handle publishes and draft posts
class Publishedmanager(models.Manager):
    def get_queryset(self):
        return super(Publishedmanager,self).get_queryset().filter(status="published")


class Post(models.Model):
    objects = models.Manager()
    published = Publishedmanager()

    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )

    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title  = models.TextField(max_length= 250)
    body   = RichTextField()
    slug   = models.SlugField(unique = True)
    image  = models.ImageField(null = True, default ="post.jpg", upload_to="post_images")
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    date_created = models.DateTimeField(auto_now_add = True)
    date_updated = models.DateTimeField(auto_now= True)
    category =  models.ForeignKey(BlogCategory, null=True, blank=True,on_delete=models.CASCADE)
   
    
    def __str__(self):
        return  self.title
        
    def snippet(self):
        return self.body[:150] + "" + "....."
        
    
    def save(self, *args, **kwargs):        
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)
    
    def get_cat_list(self):
        parent_cat = self.category 
        breadcrumb = ["dummy"]
        while  parent_cat is not None:
            breadcrumb.append( parent_cat.slug)
            parent_cat = parent_cat.parent
            
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]       

    class Meta:           
        verbose_name_plural = 'posts'
        db_table = 'posts'




class BlogComments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextField(max_length = 300)
    post = models. ForeignKey(Post, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta: 
        verbose_name_plural ='blog_comments'
        db_table = "blog_comments"
    
    def __str__(self):
        return self.text
