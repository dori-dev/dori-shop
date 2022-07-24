from django.shortcuts import render
from . import models


def index(request):
    latest_products = models.Product.objects.all()[:5]
    context = {
        'latest_products': latest_products,
    }
    return render(request, 'shop/index.html', context)


def product(request):
    return render(request, 'shop/product.html')


def store(request):
    return render(request, 'shop/store.html')


def checkout(request):
    return render(request, 'shop/checkout.html')
