from django.contrib import admin
from .models import Message


@admin.register(Message)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'receive_date')
