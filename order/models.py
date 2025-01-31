from django.db import models
from account.models import registration
from store.models import product,Veriation

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(registration,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=200,null=True,blank=True)
    amount_paid = models.CharField(max_length=200,null=True,blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    
order_status = {
    "New":"New",
    "Completed":"Completed",
    "Cancelled":"Cancelled",
    "Accepted":"Accepted",

}

class Order(models.Model):
    user = models.ForeignKey(registration,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE,null=True,blank=True)
    order_number = models.CharField(max_length=255,unique=True,null=True,blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address_line_1 = models.TextField()
    address_line_2 = models.TextField(null=True,blank=True)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    total = models.CharField(max_length=255)
    tax = models.CharField(max_length=255)
    status = models.CharField(max_length=255,choices=order_status,default="New")
    order_note = models.CharField(max_length=255,null=True,blank=True)
    ip = models.CharField(max_length=255)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    user = models.ForeignKey(registration,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Veriation, blank=True)
    quantity = models.IntegerField()
    product_price = models.CharField(max_length=100)
    is_ordedred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order.order_number