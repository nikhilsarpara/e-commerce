from django.urls import path
from .views import *

urlpatterns = [
    path('registration/',Registration,name='registration'),
    path('login/',login,name='login'),
    path('logout',logout,name='logout'),
    path('verification/<uid64>/<token>',verification,name='verification'),
    path('UserDashboard/',UserDashboard,name='UserDashboard'),
    path('UserOrders/',UserOrders,name='UserOrders'),
    path('UserOrderDetails/<ordeid>/',UserOrderDetails,name='UserOrderDetails'),
    path('forget_password/',forget_password,name='forget_password'),
    path('newpassword/',newpassword,name='newpassword'),
    path('change_password/',change_password,name='change_password'),
    path('generate-invoice/<order_id>/',generate_invoice,name='generate_invoice'),
]
