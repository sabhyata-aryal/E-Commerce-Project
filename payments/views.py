from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import requests
from customer_orders.models import Order


def esewa_payment(request):
    order_id = request.session.get('order_id')
    order_total = request.session.get('order_total')
    if not order_id or not order_total:
        return redirect('checkout')

    # eSewa sandbox URL
    esewa_url = "https://uat.esewa.com.np/epay/main"

    # Context for POST form
    context = {
        'amount': order_total,
        'tax_amount': 0,
        'total_amount': order_total,
        'product_code': order_id,
        'success_url': request.build_absolute_uri('/payments/esewa_success/'),
        'failure_url': request.build_absolute_uri('/payments/esewa_failed/'),
        'merchant_code': 'EPAYTEST',  # Sandbox merchant code
    }
    return render(request, 'payments/esewa_payment.html', context)


def esewa_success(request):
    ref_id = request.GET.get('refId')
    product_code = request.GET.get('oid')

    if not ref_id or not product_code:
        return redirect('checkout')

    # Verify payment with eSewa sandbox
    verification_url = "https://uat.esewa.com.np/epay/transrec"
    order = Order.objects.get(id=product_code)

    data = {
        'amt': order.total_price,
        'scd': 'EPAYTEST',
        'pid': product_code,
        'rid': ref_id,
    }

    response = requests.post(verification_url, data=data)
    if "Success" in response.text:
        # Payment verified successfully - order is already created with payment_method
        # Note: Order model doesn't have payment_status field, payment_method is stored instead
        return redirect('order_success')
    else:
        return redirect('esewa_failed')


def esewa_failed(request):
    return HttpResponse("<h3>❌ Payment Failed! Please try again.</h3>")
