from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from .managers import ClientManager


class Address(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, verbose_name='client',related_name='client_address', null=True)
    state = models.CharField(max_length=100, verbose_name='State')
    city = models.CharField(max_length=100, verbose_name='City')
    address = models.TextField(verbose_name='Address')

class Client(AbstractBaseUser):
    email = models.EmailField( verbose_name='Email Address',max_length=255)
    phone = models.CharField(max_length=12, verbose_name='Phone Number', unique=True)
    username = models.CharField(max_length=255, verbose_name='Username')
    profile_pic = models.ImageField(verbose_name='Profile Picture', upload_to='accounts/profile_pics')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = ClientManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin





class Otp(models.Model):
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=100)
    token = models.CharField(max_length=255)
    otp_create_at = models.DateTimeField(auto_now=True)
    expired = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=4)


    def __str__(self):
        return self.phone