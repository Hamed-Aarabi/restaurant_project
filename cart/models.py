from django.db import models
from account.models import Client

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Client Orders', related_name='orders_of_client')
    order_total_price = models.PositiveIntegerField(verbose_name='Total Price')
    address = models.TextField(verbose_name='Address of Client', default='')
    paid = models.BooleanField(default=False, verbose_name='Status of paid')
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client.phone


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Order', related_name='orders')
    food_name = models.CharField(max_length=100, verbose_name='Food Name')
    quantity = models.CharField(max_length=255, verbose_name='Quantity')
    price = models.PositiveIntegerField(verbose_name='Price of One Quantity')
    total_price = models.PositiveIntegerField(verbose_name='Price of Total')

    def __str__(self):
        return self.food_name



class Discount(models.Model):
    code = models.CharField(max_length=20, verbose_name='Discount Code')
    percent = models.PositiveSmallIntegerField(verbose_name='Percent of Discount')
    quantity = models.PositiveSmallIntegerField(verbose_name='Quantity of Discount')
    expired = models.BooleanField(default=False, verbose_name='Status of Discount')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code