from django.contrib import admin
from .models import Message, ContactUs


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'receive_date')


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address')
