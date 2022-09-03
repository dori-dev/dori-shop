from django.db import models
from django.contrib.auth.models import User

from shop.models import Product


class ProductComment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    email = models.EmailField()
    body = models.TextField()
    rate = models.FloatField(
        max_length=5,
    )
    send_at = models.DateTimeField(
        auto_now_add=True,
    )
    confirmed = models.BooleanField(
        default=False,
    )

    def save(self, *args, **kwargs):
        product = Product.objects.filter(
            id=self.product.id
        ).first()
        exists = product.comments.filter(
            user=self.user
        ).exists()
        if exists is False:
            return super().save(*args, **kwargs)
