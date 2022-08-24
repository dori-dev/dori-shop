from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from zeep import Client
from cart.forms import CartAddProductForm
from cart.cart import Cart
from . import models


merchant_code = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl/')


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


def to_bank(request: WSGIRequest, order_id):
    order = get_object_or_404(models.Order, id=order_id)
    if order.customer != request.user:
        raise Http404
    amount = sum(
        product['product_cost'] for product in
        models.OrderItem.objects.filter(
            order=order
        ).values('product_cost')
    )
    description = 'این یک تست است'
    email = ''
    mobile = ''
    callback_url = request.build_absolute_uri(reverse('shop:callback'))
    result = client.service.PaymentRequest(
        merchant_code,
        amount,
        description,
        email,
        mobile,
        callback_url
    )
    if result.Status == 100 and len(result.Authority) == 36:
        authority = result.Authority
        models.Invoice.objects.create(
            order=order,
            authority=authority
        )
        return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}')
    else:
        return HttpResponse(f'Error code: {result.Status}')


def callback(request: WSGIRequest):
    status = request.GET.get('Status')
    if status is not None and status == 'OK':
        authority = request.GET.get('Authority')
        invoice = get_object_or_404(
            models.Invoice,
            authority=authority
        )
        order = invoice.order
        amount = sum(
            product['product_cost'] for product in
            models.OrderItem.objects.filter(
                order=order
            ).values('product_cost')
        )
        result = client.service.PaymentVerification(
            merchant_code,
            authority,
            amount,
        )
        if result.Status == 100:
            context = {
                'invoice': invoice
            }
            return render(request, 'callback.html', context)
        else:
            return HttpResponse(f'Status Code: {result.Status}')
    else:
        return HttpResponse(f'Error: {status}')
