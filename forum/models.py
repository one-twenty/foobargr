from django.db import models
from django.conf import settings
from datetime import datetime    
from tinymce import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True, unique=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Topic(models.Model):
    title = models.CharField(max_length=200) 
    content = HTMLField('Content')
    category = models.ForeignKey(Category, verbose_name='Category', default=0, on_delete=models.SET_DEFAULT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=0, on_delete=models.SET_DEFAULT)
    datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Topics'

    def __str__(self):  
        return self.title


class Post(models.Model):
    content = HTMLField('Content')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=0, on_delete=models.SET_DEFAULT)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'Post from: {self.user} on {self.topic}'


class Reply(models.Model):
    content = HTMLField('Content')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=0, on_delete=models.SET_DEFAULT)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Replies'

    def __str__(self):
        return f'Reply from: {self.user} on {self.post}'
