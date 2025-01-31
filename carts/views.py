from django.shortcuts import render,redirect ,get_object_or_404
from store.models import product
from django.http import HttpResponse
from carts.models import *
from store.models import *
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .models import WishList


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if cart is None:
        cart = request.session.create()
    return cart

def add_to_cart(request,product_id):

    Product = product.objects.get(id=product_id)

    product_variations = []
    if request.method == 'POST':
        for item in request.POST:      
            key = item
            value = request.POST[key]
            
            try:
                Variation = Veriation.objects.get(Product=Product,Veriation_category__iexact=key,Veriation_value__iexact=value)
                product_variations.append(Variation)
            except:
                pass

    if request.user.is_authenticated:
        
        cart_items = CartItem.objects.filter(product=Product, user=request.user)
        
        for cart_item in cart_items:
            existing_variations = list(cart_item.variation.all())
            if set(product_variations) == set(existing_variations):
                cart_item.quantity += 1
                cart_item.save()
                break
        else:
            # Create a new cart item if no matching variations exist
            cart_item = CartItem.objects.create(
                product=Product,
                user=request.user,
                quantity=1,
            )
            if product_variations:
                cart_item.variation.add(*product_variations)

    else:

        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

        # Check if the product with the same variations exists in the cart
        cart_items = CartItem.objects.filter(product=Product, cart=cart)
        
        for cart_item in cart_items:
            existing_variations = list(cart_item.variation.all())
            if set(product_variations) == set(existing_variations):
                cart_item.quantity += 1
                cart_item.save()
                break
        else:
            # Create a new cart item if no matching variations exist
            cart_item = CartItem.objects.create(
                product=Product,
                cart=cart,
                quantity=1
            )
            if product_variations:
                cart_item.variation.add(*product_variations)

    return redirect('cart')

def plus(request,product_id,cart_item_id):
    pro = product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(id=cart_item_id,product=pro,user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(id=cart_item_id,product=pro,cart=cart)

    cart_item.quantity += 1
    cart_item.save()
            
    return redirect('cart')

def cart(request):
    total = 0

    try:
        cart_items = CartItem.objects.filter(user=request.user)
    except:
        cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))

    for i in cart_items:
        total += (i.product.product_price * i.quantity)

    text = (2*total)/100 

    grand_total = text + total

    context = {
        'cart_items':cart_items,
        'total':total,
        'text':text,
        'grand_total':grand_total
    }

    return render(request,'store/cart.html',context)

def decrease(request,product_id,cart_item_id):
    pro = product.objects.get(id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=cart_item_id,product=pro,user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(id=cart_item_id,product=pro,cart=cart)
        # cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart_item = CartItem.objects.get(product=pro,cart=cart,id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()
            
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')

@login_required(login_url='login')
def cheakout(request):
    return render(request,'store/cheakout.html')


@login_required(login_url='login')
def add_to_wishlist(request):
    product_id = request.GET.get('product_id')
    Product = get_object_or_404(product, id=product_id)

    # Check if already in wishlist
    wishlist_item, created = WishList.objects.get_or_create(user=request.user, Product=Product)

    if created:
        messages.success(request, "Product added to your wishlist!")
    else:
        messages.info(request, "Product is already in your wishlist.")

    return redirect('store')

@login_required(login_url='login')
def remove_from_wishlist(request, product_id):
    wishlist_item = WishList.objects.filter(user=request.user, product_id=product_id).first()

    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, "Product removed from your wishlist.")
    else:
        messages.error(request, "Product not found in your wishlist.")

    return redirect('wishlist')

@login_required(login_url='login')
def wishlist(request):
    wishlist_items = WishList.objects.filter(user=request.user)
    context={
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)

    