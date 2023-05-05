from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, status
from django.contrib.auth.models import User
from rest_framework.templatetags.rest_framework import data

from .models import TradingPoint, Employee, Order, Visit

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

    def validate(self, attrs):

        orderer = attrs.get('orderer')
        trade_point_id = attrs.get('trade_point_id')
        created_time = attrs.get('createTime')

        visitorder = Visit.objects.filter(where_id=trade_point_id, author_id=orderer).first()
        if not isinstance(visitorder, Visit) or created_time > timezone.now().time():
            raise serializers.ValidationError(str(trade_point_id) + '\nНевозможно создать посещение для этого заказа ' + str(orderer))
        return attrs


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