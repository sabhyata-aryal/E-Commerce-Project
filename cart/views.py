from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .cart import Cart
from django.http import JsonResponse


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1

        cart.add(product=product, quantity=quantity)

        # Use cart.cart.values() to avoid Decimal serialization issue
        cart_count = sum(item['quantity'] for item in cart.cart.values())

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'{product.name} added to cart.',
                'cart_count': cart_count
            })

        return redirect('cart_detail')

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def increase_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.increase_quantity(product)
    return redirect('cart_detail')


def decrease_quantity(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrease_quantity(product)
    return redirect('cart_detail')
