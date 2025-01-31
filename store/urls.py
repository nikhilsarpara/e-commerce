from django.urls import path
from store.views import *
from account.views import *

urlpatterns = [
    path('',store,name='store'),

    path('<category_slug>/',store,name='product_by_category'),

    path('<category_slug>/<product_slug>/',product_detail,name='product_detail'),

    path('search',search,name='search'),   
]
