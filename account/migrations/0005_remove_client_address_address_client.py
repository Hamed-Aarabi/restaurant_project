# Generated by Django 4.1.7 on 2023-03-08 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_address_client_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_address', to=settings.AUTH_USER_MODEL, verbose_name='Address'),
        ),
    ]