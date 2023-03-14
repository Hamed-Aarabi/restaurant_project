from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Client


class AuthWithUsername(BaseBackend):
    def authenticate(self, request,username=None, password=None, **kwargs):
        try:
            user = Client.objects.get(username=username)
            if user.check_password(password):
                return user
            return None
        except Client.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Client.objects.get(pk=user_id)
        except Client.DoesNotExist:
            return None


class AuthWithEmail(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Client.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except Client.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Client.objects.get(pk=user_id)
        except Client.DoesNotExist:
            return None