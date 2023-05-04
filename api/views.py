from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from api import serializer
from django.contrib.auth.models import User
from .models import TradingPoint, Order
from .serializer import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import TradePointsSerializer
from rest_framework.decorators import api_view


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializer.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializer.UserSerializer


class TradingPointViewSet(generics.ListAPIView):
    queryset = TradingPoint.objects.all()
    serializer_class = serializer.TradePointsSerializer


class TradePointListView(APIView):
    def get_employee_phone_number(self, request):
        return request.GET.get('phone_number')

    def get_trade_points(self, phone_number):
        return TradingPoint.objects.filter(employee__phone_number=phone_number)

    def get(self, request):
        phone_number = self.get_employee_phone_number(request)
        trade_points = self.get_trade_points(phone_number)
        serializer = TradePointsSerializer(trade_points, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)


@api_view(['POST'])
def add_items(request):
    order = OrderSerializer(data=request.data)

    if order.is_valid():
        order.save()
        return Response(order.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_items(request, pk):
    orders = Order.objects.get(pk=pk)
    data = OrderSerializer(instance=orders, data=request.data)

    if data.is_valid():
        data.save()
        return Response(request.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_items_status(request, pk):
    orders = Order.objects.get(pk=pk)
    data = OrderSerializer(instance=orders, data=request.data)

    if data.is_valid():
        data.save()
        return Response(request.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_items(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def view_items(request):
    # checking for the parameters from the URL
    if request.query_params:
        orders = Order.objects.filter(**request.query_params.dict())
    else:
        orders = Order.objects.all()

    # if there is something in items else raise error
    if orders:
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.orderer)