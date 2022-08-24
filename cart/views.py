from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.core.handlers.wsgi import WSGIRequest
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def cart_detail(request: WSGIRequest):
    cart = Cart(request)
    for item in cart:
        item['update_product_count_form'] = CartAddProductForm(
            initial={
                'product_count': item['product_count'],
                'update': True
            }
        )
    context = {
        'cart': cart
    }
    return render(request, 'cart/detail.html', context)


@require_POST
def cart_add(request: WSGIRequest, product_id: int):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cart_data = form.cleaned_data
        cart.add(
            product=product,
            product_count=cart_data['product_count'],
            update_count=cart_data['update']
        )
    return redirect('cart:cart_detail')


def cart_remove(request: WSGIRequest, product_id: int):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
