from django.db import models
from froala_editor.fields import FroalaField
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from .helpers import *

# Create your models here.



class Blog(models.Model):
    title = models.CharField(max_length=1000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Blog, self).save(*args, **kwargs)

    def snippet(self):
        return self.content[:50] + '...'
    



    
    

