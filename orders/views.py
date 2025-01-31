from django.shortcuts import render
from django.http import JsonResponse
from orders.models import *
from carts.models import *
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
# Create your views here.

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

@csrf_exempt
def payment(request):
    data = json.loads(request.body)

    payment_id = data["razorpay_payment_id"]
    useremail = request.user.email

    order = Order.objects.get(user=request.user,is_ordered=False,order_number=data['Order'])

    try:
        payment = Payment(
            user=request.user,
            payment_id=payment_id,
            payment_method="Razorpay",
            amount_paid=data['Amount'],
            status=True
        )
        payment.save()

        order.payment = payment
        order.is_ordered = True
        order.save()

        cart_item = CartItem.objects.filter(user=request.user)

        for item in cart_item:
            parchsedproduct = OrderProduct()
            parchsedproduct.order = order
            parchsedproduct.user = request.user
            parchsedproduct.payment = payment
            parchsedproduct.product = item.product
            parchsedproduct.quantity = item.quantity
            parchsedproduct.product_price = item.product.product_price
            parchsedproduct.is_ordedred = True

            parchsedproduct.save()

            parchsedproduct.variations.set(item.variation.all())
            parchsedproduct.save()

            product = item.product
            if product.product_stock >= item.quantity:
                product.product_stock -= item.quantity
                product.save()

        cart_item.delete()

        try:
            email_subject = "Thank Your For Your Order."
            current_side = get_current_site(request)

            context = {
                'user':request.user,
                'domain':current_side,
                'order':order,
            }
            message = render_to_string('order/order_confirm.html',context)
            send_email = EmailMessage(email_subject,message,to=[useremail])
            send_email.send()

        except:
            pass

        ds = {
        "success":True,
        "OrderId":order.order_number,
        }
        return JsonResponse(ds)

    except:
        pass

def place_order(request):
    total = 0

    cart_items = CartItem.objects.filter(user=request.user)

    for i in cart_items:
        total += (i.product.product_price * i.quantity)

    text = (2*total)/100 

    grand_total = text + total

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        order_note = request.POST['order_note']

        new_order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            country=country,
            state=state,
            city=city,
            order_note=order_note,
            tax=text,
            total=grand_total,
            ip = request.META.get('REMOTE_ADDR')
        )

        today = date.today()
        formatted_date = today.strftime("%d%m%Y") + str(new_order.id)
        new_order.order_number = formatted_date
        new_order.save() 

        client = razorpay.Client(auth=("rzp_test_susforIvG6nYky","VUQ8dfvBSkVS9Lstz9r1pQ9r"))

        razorpay_client = client.order.create({
            "amount":int(grand_total * 100),
            "currency":"INR",
            "receipt":"order_number",
            "payment_capture":1,
        })

        context = {
            'cart_items':cart_items,
            'text':text,
            'grand_total':grand_total,
            'order':new_order,
            'razorpay_order_id':razorpay_client['id'],
            'key':"rzp_test_susforIvG6nYky",
            'amounts':razorpay_client['amount']
        }

        return render(request,'order/payment.html',context)
    

def order_complete(request):

    try:
        orderid = request.GET.get("ordernumber")
        order = Order.objects.get(order_number=orderid)

        order_products = OrderProduct.objects.filter(order=order)

        grand_total = float(order.total)
        tax = float(order.tax)
        address_line_1 = order.address_line_1
        address_line_2 = order.address_line_2
        city = order.city
        country = order.country
        first_name = order.first_name
        last_name = order.last_name



        print(order)
    except:
        pass

    context = {
        'order':order,
        'grand_total':grand_total,
        'tax':tax,
        'address_line_1':address_line_1,
        'address_line_2':address_line_2,
        'city':city,
        'country':country,
        'first_name':first_name,
        'last_name':last_name,
        'order_products':order_products,
    }

    return render(request,"order/order_complete.html",context)