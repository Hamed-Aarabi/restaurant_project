from django.db import models

class Message(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255)
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(verbose_name='Phone', max_length=12)
    message = models.TextField(verbose_name='Message')
    receive_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




