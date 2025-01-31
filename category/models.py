from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    image = models.ImageField(upload_to='category_image')

    def __str__(self):
        return self.category_name
    
    def get_url(self):
        return reverse('product_by_category',args=[self.slug])