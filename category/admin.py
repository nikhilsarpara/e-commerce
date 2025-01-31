from django.contrib import admin
from category.models import *
# Register your models here.

class AdminCategory(admin.ModelAdmin):
    list_display = ['category_name']
    prepopulated_fields = {'slug':('category_name',)}

admin.site.register(Category,AdminCategory)