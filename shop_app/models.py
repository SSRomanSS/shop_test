from django.db import models
from django.core.exceptions import ValidationError


def validate_name(value):
   if len(value) < 3:
      raise ValidationError(f'Name "{value}" has less then 3 symbols')


def validate_price(value):
   if value <= 0:
      raise ValidationError('Price must be positive')


class Order(models.Model):
    """Model for order"""
    class Meta(object):
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['user']

    name = models.CharField(max_length=64, validators=[validate_name])
    price = models.IntegerField(validators=[validate_price])
    user = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name} costs {self.price} ordered by {self.user}'
