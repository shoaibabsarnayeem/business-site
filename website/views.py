from django.shortcuts import render, redirect
from .models import Contact

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "services.html")

def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            message=request.POST["message"]
        )
        return redirect("contact")
    return render(request, "contact.html")


from django.shortcuts import redirect, get_object_or_404
from .models import Product

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart = request.session.get('cart', {})

    pid = str(product.id)

    if pid in cart:
        cart[pid]['qty'] += 1
    else:
        cart[pid] = {
            'qty': 1,
            'price': float(product.price)  # 🔥 IMPORTANT
        }

    request.session['cart'] = cart
    return redirect('cart')
from .models import Product

def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for pid, item in list(cart.items()):
        try:
            product = Product.objects.get(id=pid)
        except Product.DoesNotExist:
            del cart[pid]           # remove broken item
            request.session['cart'] = cart
            continue

        subtotal = product.price * item['qty']
        total += subtotal

        products.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'qty': item['qty'],
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })

from django.shortcuts import render
from .models import Product

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})
    


def remove_from_cart(request, product_id):
    cart = request.session.get('cart')

    if not cart or isinstance(cart, list):
        cart = {}

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

def increase_qty(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['qty'] += 1

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


def decrease_qty(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id]['qty'] -= 1
        if cart[product_id]['qty'] <= 0:
            del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

def checkout(request):
    return render(request, 'checkout.html')

from .models import Order

def checkout(request):
    cart = request.session.get('cart', {})

    for item in cart.values():
        Order.objects.create(
            name=item['name'],                     # ✅ NOW EXISTS
            price=item['price'],
            qty=item['qty'],
            subtotal=item['price'] * item['qty']
        )

    request.session['cart'] = {}
    return render(request, 'checkout.html')

import razorpay
from django.conf import settings

def payment(request):
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    amount = 50000  # ₹500
    payment = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'
    })

    return render(request, 'payment.html', {
        'payment': payment,
        'key': settings.RAZORPAY_KEY_ID
    })

from .models import Product

def checkout(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for pid, item in cart.items():
        try:
            product = Product.objects.get(id=pid)
        except Product.DoesNotExist:
            continue

        subtotal = product.price * item['qty']
        total += subtotal

        items.append({
            'name': product.name,
            'price': product.price,
            'qty': item['qty'],
            'subtotal': subtotal
        })

    return render(request, 'checkout.html', {
        'items': items,
        'total': total
    })
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total = sum(item['price'] * item['qty'] for item in cart.values())
    order = Order.objects.create(total=total)

    for item in cart.values():
        OrderItem.objects.create(
            order=order,
            product_name=item['name'],
            qty=item['qty'],
            price=item['price']
        )

    request.session['cart'] = {}
    return redirect('order_success')

def order_success(request):
    return render(request, 'order_success.html')