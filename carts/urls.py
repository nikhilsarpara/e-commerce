from django.urls import path
from carts.views import *

urlpatterns = [
    path('',cart,name='cart'),
    path('add_to_cart/<product_id>',add_to_cart,name='add_to_cart'),
    path('decrease/<product_id>/<cart_item_id>',decrease,name='decrease'),
    path('plus/<product_id>/<cart_item_id>',plus,name='plus'),
    path('wishlist/',wishlist,name='wishlist'),
    path('add_to_wishlist/',add_to_wishlist,name='add_to_wishlist'),
    path('remove_from_wishlist/',remove_from_wishlist,name='remove_from_wishlist'),
    path('cheakout',cheakout,name='cheakout'),
]
