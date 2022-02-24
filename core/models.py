from django.db import models

# Create your models here.

class ContactMessage(models.Model):
    first_name = models.CharField( max_length=200, blank = False)
    last_name = models.CharField( max_length=200, blank = False)
    email= models.EmailField(blank = False, null = False)
    phone= models.CharField(max_length =15, blank = False, null = False)
    subject= models.CharField(max_length=200, blank = False)
    message = models.TextField(blank = False, null = False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name, self.email