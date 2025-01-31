from django.contrib import admin
from carts.models import *
# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishList)