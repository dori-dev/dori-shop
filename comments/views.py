from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.handlers.wsgi import WSGIRequest

from .models import ProductComment
from shop.models import Product
from .forms import ProductCommentForm


def int_or_default(value: str, default: int = 5) -> int:
    if value.isdigit():
        return int(value)
    return default


@require_POST
def send_product_comment(request: WSGIRequest, pk: int):
    product = get_object_or_404(Product, pk=pk)
    allow = product.allow_to_send_comment(request.user)
    redirect_page = redirect('shop:product', slug=product.slug)
    if not allow:
        return redirect_page
    form = ProductCommentForm(request.POST)
    if form.is_valid():
        body = form.cleaned_data.get('body')
        rate = request.POST.get('rate')
        if rate is None or rate == '0':
            rate = 5
        ProductComment.objects.create(
            user=request.user,
            product=product,
            body=body,
            rate=int_or_default(rate),
        )
    return redirect_page
