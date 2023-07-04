from django.urls import path

from orders.views import (OrderDetailView, OrderListView, OrdersCreateView,
                          SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('create/', OrdersCreateView.as_view(), name='order_create'),
    path('success/', SuccessTemplateView.as_view(), name='order_success'),
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order'),
]
