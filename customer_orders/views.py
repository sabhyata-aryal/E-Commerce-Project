from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from customer_orders.models import Order, OrderItem
from cart.cart import Cart

from decimal import Decimal
import requests

from django.urls import reverse


# =============================
# CHECKOUT
# =============================
def checkout(request):
    cart = Cart(request)

    if not cart:
        return redirect('cart_detail')

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Decimal (SAFE for DB)
        total_price = cart.get_total_price()

        # Create order
        order = Order.objects.create(
            customer_name=name,
            email=email,
            phone=phone,
            address=address,
            payment_method=payment_method,
            total_price=total_price,
            payment_status='paid' if payment_method == 'cod' else 'pending'
        )

        # Save order items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=Decimal(item['price']),  # ensure Decimal
            )

        # SESSION MUST BE JSON SAFE
        request.session['order_id'] = int(order.id)

        # =============================
        # COD FLOW
        # =============================
        if payment_method == 'cod':
            _send_order_emails(order)
            cart.clear()
            return redirect('order_success')

        # =============================
        # KHALTI FLOW
        # =============================
        return redirect('khalti_initiate')

    return render(request, 'customer_orders/checkout.html')


# =============================
# KHALTI INITIATE
# =============================
def khalti_initiate(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    url = "https://a.khalti.com/api/v2/epayment/initiate/"

    amount_in_paisa = int(order.total_price * 100)

    payload = {
        "return_url": request.build_absolute_uri(
            reverse("khalti_callback")
        ),
        "website_url": request.build_absolute_uri("/"),
        "amount": amount_in_paisa,
        "purchase_order_id": str(order.id),
        "purchase_order_name": f"Nature Touch Order #{order.id}",
        "customer_info": {
            "name": order.customer_name,
            "email": order.email,
            "phone": order.phone,
        }
    }

    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if response.status_code == 200:
        return redirect(data["payment_url"])

    return JsonResponse(data, status=400)


# =============================
# KHALTI CALLBACK
# =============================
def khalti_callback(request):
    pidx = request.GET.get("pidx")

    if not pidx:
        return redirect("checkout")

    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://a.khalti.com/api/v2/epayment/lookup/",
        json={"pidx": pidx},
        headers=headers,
    )

    data = response.json()

    if data.get("status") == "Completed":
        order_id = request.session.get("order_id")

        if not order_id:
            return redirect("checkout")

        order = get_object_or_404(Order, id=order_id)

        if order.payment_status != "paid":
            order.payment_status = "paid"
            order.save()

            _send_order_emails(order)
            Cart(request).clear()

        return redirect("order_success")

    return redirect("checkout")
 



# ============================
# EMAIL SENDER
# =============================
def _send_order_emails(order):
    # CUSTOMER EMAIL
    html_message = render_to_string(
        'customer_orders/order_email.html',
        {
            'customer_name': order.customer_name,
            'cart': order.items.all(),
            'total_price': order.total_price,
            'order_id': order.id,
            'payment_method': order.payment_method.upper(),
        }
    )

    send_mail(
        subject=f"Your Order Confirmation - Nature Touch (Order #{order.id})",
        message="Please view this email in HTML format.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.email],
        html_message=html_message,
        fail_silently=False,
    )

    # ADMIN EMAIL
    items = []
    for item in order.items.all():
        line_total = item.price * item.quantity
        items.append(
            f"- {item.product.name} x{item.quantity} = Rs. {line_total}"
        )

    admin_message = f"""
NEW ORDER RECEIVED

Order ID: {order.id}
Date: {timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")}
Payment Method: {order.payment_method.upper()}

Customer:
Name: {order.customer_name}
Phone: {order.phone}
Address: {order.address}

Items:
{chr(10).join(items)}

Total: Rs. {order.total_price}
"""

    send_mail(
        subject=f"New Order #{order.id} - Nature Touch",
        message=admin_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['naturetouchmatkarestro@gmail.com'],
        fail_silently=True,
    )


# =============================
# ORDER SUCCESS
# =============================
def order_success(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'customer_orders/order_success.html', {
        'email': order.email,
        'total_price': order.total_price,
    })
