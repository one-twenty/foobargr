from django.db import models
from django.conf import settings
from datetime import datetime    

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    parent_category = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class Topic(models.Model):
    topic_title = models.CharField(max_length=200) 
    topic_content = models.TextField()
    topic_category = models.ForeignKey(Category, verbose_name='Category', default=0, on_delete=models.SET_DEFAULT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=0, on_delete=models.SET_DEFAULT)
    datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Topics'

    def __str__(self):  
        return self.topic_title


class Post(models.Model):
    post_content = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=0, on_delete=models.SET_DEFAULT)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f'Post from: {self.user} on {self.topic}'


class Reply(models.Model):
    reply_content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=0, on_delete=models.SET_DEFAULT)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Replies'

    def __str__(self):
        return f'Reply from: {self.user} on {self.post}'
