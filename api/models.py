from django.db import models
from .status_choices import StatusChoice


class TradingPoint(models.Model):
    name = models.CharField(max_length=255)
    workers = models.ForeignKey('Employee', on_delete=models.CASCADE, blank=True, null=True)


class Employee(models.Model):
    phone_number = models.CharField(max_length=255)
    trading_points = models.ForeignKey('TradingPoint', on_delete=models.CASCADE, null=True, blank=True)

    # @property
    # def __str__(self):
    #     return self.phone_number


class Order(models.Model):
    customer = models.ForeignKey('Orderer', on_delete=models.CASCADE, blank=True, null=True)
    store = models.ForeignKey('TradingPoint', on_delete=models.CASCADE, blank=True, null=True)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(choices=StatusChoice.choices, default=StatusChoice.AWAITING, max_length=255, null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()



class Orderer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    trading_points = models.ForeignKey('TradingPoint', on_delete=models.CASCADE, null=True, blank=True)

