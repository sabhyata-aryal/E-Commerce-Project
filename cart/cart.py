from decimal import Decimal
from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)  
            }

        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def increase_quantity(self, product):
        """
        Increase product quantity by 1.
        """
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] += 1
            self.save()

    def decrease_quantity(self, product):
        """
        Decrease product quantity by 1.
        Remove product if quantity becomes 0.
        """
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1

            if self.cart[product_id]['quantity'] <= 0:
                self.remove(product)
            else:
                self.save()

    def save(self):
        """
        Mark the session as modified to make sure it is saved.
        """
        self.session.modified = True

    def clear(self):
        """
        Remove cart from session.
        """
        self.session['cart'] = {}
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over cart items safely without mutating session data.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()  

        for product in products:
            item = cart[str(product.id)].copy() 
            item['product'] = product
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count total items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate total cart price.
        """
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
