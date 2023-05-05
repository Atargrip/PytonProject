from django.contrib import admin

# Register your models here.
from .models import (Employee, TradingPoint, Order, Orderer, Visit)

admin.site.register(Employee)
admin.site.register(TradingPoint)
admin.site.register(Order)
admin.site.register(Orderer)
admin.site.register(Visit)