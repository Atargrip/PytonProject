from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, status
from django.contrib.auth.models import User
from .models import TradingPoint, Employee, Order, Visit, Orderer
import json

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

class OrdererSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class VisitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ('id', 'order', 'employee', 'date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

    def validate(self, data):

        orderer = data.get('author')

        trade_point = data.get('where')
        created_time = data.get('createTime')
        order = data.get('order')
        employee = data.get('performer')

        if orderer.trading_points_id != trade_point.id or order.updated_at < created_time:
            raise serializers.ValidationError("Вы не можете создовать посешение" + str(json.dumps(data, indent=4, sort_keys=True, default=str)))
        elif Visit.objects.filter(order=order).exists():
            raise serializers.ValidationError("Посешение уже существует")
        elif employee.id != order.employee.id:
            raise serializers.ValidationError(" Этот работник не привязан к заказу")
        return data

    def create(self, validated_data):
        order = validated_data.get('order')
        author = validated_data.get('author')
        where = validated_data.get('where')
        performer = validated_data.get('performer')
        createTime = validated_data.get('createTime')


        instance = Visit.objects.create(
            order = order,
            author = author,
            where = where,
            performer = performer,
            createTime = createTime
        )

        instance.save()
        return instance