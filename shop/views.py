from decimal import Decimal
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from cart.forms import CartAddProductForm
from cart.cart import Cart
from . import models


def index(request):
    latest_products = models.Product.objects.all()[:5]
    context = {
        'latest_products': latest_products,
    }
    return render(request, 'shop/index.html', context)


def product(request, pk: int):
    product_object = get_object_or_404(models.Product, id=pk)
    form = CartAddProductForm()
    context = {
        'product': product_object,
        'form': form
    }
    return render(request, 'shop/product.html', context)


def store(request):
    return render(request, 'shop/store.html')


@login_required
def checkout(request: WSGIRequest):
    if request.method == 'POST':
        cart = Cart(request)
        order = models.Order.objects.create(
            customer=request.user
        )
        for item in cart:
            models.OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_price=item['price'],
                product_count=item['product_count'],
                product_cost=Decimal(item['total_price'])
            )
        cart.clear()
        context = {
            'order': order,
        }
        return render(request, 'shop/order.html', context)
    return render(request, 'shop/checkout.html')
