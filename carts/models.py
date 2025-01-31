from django.db import models
from store.models import *
from account.models import *
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=255,null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(registration,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    variation = models.ManyToManyField(Veriation,blank=True)

    def sub_total(self):
        return self.product.product_price * self.quantity
    
    def __str__(self):
        return self.product.product_name
    
class WishList(models.Model):
    user = models.ForeignKey(registration,on_delete=models.CASCADE,blank=True,null=True)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlist entries


    def __str__(self):
        return self.product.product_name
