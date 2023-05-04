from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TradingPoint, Employee, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'phone_number')


class TradePointsSerializer(serializers.ModelSerializer):
    workers = WorkerSerializer()

    class Meta:
        model = TradingPoint
        fields = ('id', 'name', 'workers')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

