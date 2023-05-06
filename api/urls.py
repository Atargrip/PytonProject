from django.urls import path
from api import views

urlpatterns = [
    path('points/', views.TradingPointViewSet.as_view()),
    path('trade_points/', views.TradePointListView.as_view(), name='trade_points'),
    path('create/', views.add_items, name='add-items'),
    path('all/', views.view_items, name='view_items'),
    path('users/', views.UserList.as_view()),
    path('visits/', views.ListVisitMixin.as_view(), name='Visit List'),
    path('details/<int:pk>', views.DetailedVisitMixins.as_view()),
    path('update/<int:pk>/', views.update_items, name='update-items'),
    path('order/<int:pk>/delete/', views.delete_items, name='delete-items'),
    path('order/<int:pk>/status', views.update_items_status)
]
