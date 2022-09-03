from .models import WishProduct


def wish(request):
    all_wish = WishProduct.objects.filter(
        user=request.user
    )
    return {
        'wish': all_wish,
        'wish_price': sum(
            wish.product.price for wish in all_wish
        ),
    }
