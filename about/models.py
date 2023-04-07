from django.db import models


class About(models.Model):
    banner = models.CharField(verbose_name='Banner', max_length=255)
    title = models.CharField(verbose_name='Title', max_length=2550)
    introduction = models.TextField(verbose_name='Introduction')
    image = models.ImageField(upload_to='about')

    def __str__(self):
        return self.banner