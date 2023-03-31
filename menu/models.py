from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    image = models.ImageField(upload_to='menu/foods', verbose_name='Image')
    price = models.CharField(max_length=20, verbose_name='Price')
    status = models.BooleanField(default=True, verbose_name='Status')

    def __str__(self):
        return self.name



