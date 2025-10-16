from .cart import Cart

def cart_context(request):
    cart = Cart(request)
    return {
        'cart_count': sum(item['quantity'] for item in cart)
    }

