from django.db import models
from django.contrib.auth.models import User


class ProductComment(models.Model):
    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    rate = models.PositiveSmallIntegerField(
        default=5,
    )
    send_at = models.DateTimeField(
        auto_now_add=True,
    )
    confirmed = models.BooleanField(
        default=False,
    )

    def save(self, *args, **kwargs):
        if self.rate > 5:
            self.rate = 5
        if self.rate < 0:
            self.rate = 0
        return super().save(*args, **kwargs)
