# Generated by Django 4.1.7 on 2023-03-26 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(default='', verbose_name='Address of Client'),
        ),
    ]
