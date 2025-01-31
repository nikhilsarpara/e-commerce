from django.contrib import admin
from .models import *
# Register your models here.

class AdminProduct(admin.ModelAdmin):
    list_display = ['product_name']
    prepopulated_fields = {'slug':('product_name',)}

admin.site.register(product,AdminProduct)

admin.site.register(Veriation)
