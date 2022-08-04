from django.shortcuts import get_object_or_404, render
from cart.forms import CartAddProductForm
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


def checkout(request):
    return render(request, 'shop/checkout.html')
