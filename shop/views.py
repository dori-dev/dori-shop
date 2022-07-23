from django.shortcuts import render


def index(request):
    return render(request, 'shop/index.html')


def product(request):
    return render(request, 'shop/product.html')


def store(request):
    return render(request, 'shop/store.html')


def checkout(request):
    return render(request, 'shop/checkout.html')
