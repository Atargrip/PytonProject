from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, mixins
from api import serializer
from django.contrib.auth.models import User
from .models import TradingPoint, Order, Visit
from .serializer import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import TradePointsSerializer, VisitSerializer
from rest_framework.decorators import api_view, action

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
    if request.query_params:
        orders = Order.objects.filter(**request.query_params.dict())
    else:
        orders = Order.objects.all()

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


class ListVisits(APIView):
    def get(self, request):
        query = Visit.objects.all()
        serializer_class = VisitSerializer(query, many=True)
        return Response(serializer_class.data)

class ListVisitMixin(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class DetailedVisitMixins(mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          generics.GenericAPIView):

    queryset = Visit.objects.all()
    serializer_class = VisitSerializer


    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if action == 'create':
            serializer_class = VisitSerializer

        return serializer_class

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(data={"results": request.data}, status=status.HTTP_201_CREATED)
        # return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)