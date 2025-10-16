from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from customer_orders.models import Order, OrderItem
from cart.cart import Cart  


# =============================
# Checkout (COD / eSewa Start)
# =============================
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse
from customer_orders.models import Order, OrderItem
from cart.cart import Cart


def checkout(request):
    cart = Cart(request)  

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        total_price = cart.get_total_price()

        # Create the order
        order = Order.objects.create(
            customer_name=name,
            email=email,
            phone=phone,
            address=address,
            payment_method=payment_method,
            total_price=total_price,
        )

        # Add order items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
            )

        # Send customer HTML email
        subject = f"Your Order Confirmation - Nature Touch (Order #{order.id})"
        html_message = render_to_string('customer_orders/order_email.html', {
            'customer_name': name,
            'cart': cart,
            'total_price': total_price,
            'order_id': order.id,
            'payment_method': payment_method.upper(),
        })
        send_mail(
            subject=subject,
            message="Please view this email in HTML format.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        # Send admin plain-text email
        now = timezone.localtime().strftime("%Y-%m-%d %H:%M:%S")
        admin_lines = []
        for item in cart:
            admin_lines.append(
                f"- {item['product'].name} (x{item['quantity']}) — Rs. {item['price'] * item['quantity']}"
            )

        admin_message = (
            f"NEW ORDER RECEIVED!\n\n"
            f"Order ID: {order.id}\n"
            f"Date: {now}\n"
            f"----------------------------------\n"
            f"Customer Info:\n"
            f"Name: {name}\n"
            f"Phone: {phone}\n"
            f"Email: {email}\n"
            f"Address: {address}\n"
            f"----------------------------------\n\n"
            f"Items:\n" + "\n".join(admin_lines) +
            f"\n\n----------------------------------\n"
            f"Total: Rs. {total_price}\n"
            f"Payment Method: {payment_method.upper()}\n"
            f"----------------------------------\n"
        )

        send_mail(
            subject=f"New Order #{order.id} from {name}",
            message=admin_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['naturetouchmatkarestro@gmail.com'],
            fail_silently=True,
        )

        # Clear the cart
        cart.clear()

        # Render success page
        return render(request, 'customer_orders/order_success.html', {
            'email': email,
            'total_price': total_price,
            'order_id': order.id
        })

    return render(request, 'customer_orders/checkout.html')

# =============================
# eSewa Payment Simulation
# =============================
def esewa_payment(request):
    order_id = request.session.get('order_id')
    order_total = request.session.get('order_total')

    return HttpResponse(f"""
        <h2 style='text-align:center;margin-top:50px;'>eSewa Sandbox Payment Demo</h2>
        <p style='text-align:center;'>This would normally redirect to eSewa.</p>
        <p style='text-align:center;'>Click below to simulate success:</p>
        <div style='text-align:center;margin-top:20px;'>
            <a href='/orders/success/' style='background:green;color:white;padding:10px 20px;border-radius:8px;text-decoration:none;'>✅ Simulate Successful Payment</a>
        </div>
    """)


# =============================
# Order Success Page
# =============================
def order_success(request):
    email = request.GET.get('email', '') or request.session.get('customer_email', '')
    total_price = request.GET.get('total_price', '') or request.session.get('order_total', 0)

    return render(request, 'customer_orders/order_success.html', {
        'email': email,
        'total_price': total_price,
    })
