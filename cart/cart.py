from decimal import Decimal
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from shop.models import Product


class Cart:
    def __init__(self, request: WSGIRequest):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if cart is None:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, product_count=1, update_count=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_count': 0,
                'price': str(product.price)}
        if update_count:
            self.cart[product_id]['product_count'] = product_count
        else:
            self.cart[product_id]['product_count'] = product_count
        self.save()

    def remove(self, product: Product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def __iter__(self):
        # TODO Optimize This(dont get(filter) product ids and product)
        # Implement these in add()
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['price'] = int(Decimal(item['price']))
            item['total_price'] = item['price'] * item['product_count']
            yield item

    def __len__(self):
        return sum(item['product_count'] for item in self.cart.values())

    def get_total_price(self):
        # TODO
        return sum(int(Decimal(item['total_price'])) for item in self.cart.values())

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
