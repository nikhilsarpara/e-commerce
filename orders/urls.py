from django.urls import path
from orders.views import *

urlpatterns = [
    path('place_order/',place_order,name='orderproduct'),
    path('payment/',payment,name='payment'),
    path('order_complete/',order_complete,name='order_complete'),
]
