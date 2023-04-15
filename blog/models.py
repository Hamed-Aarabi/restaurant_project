from django.db import models

from account.models import Client


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title', unique=True)
    body = models.TextField(verbose_name='Body')
    image = models.ImageField(verbose_name='Image', upload_to='Blog')
    date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(Client, related_name='user_blog_liked', default=0, editable=False)

    def __str__(self):
        return self.title

    def like_counter(self):
        return self.like.all().count()

    like_counter.short_description = 'likes'
