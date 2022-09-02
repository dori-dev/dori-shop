from random import choices
from string import ascii_letters

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField


class Product(models.Model):
    name = models.CharField(
        max_length=128,
    )
    slug = models.CharField(
        max_length=4,
        editable=False,
        unique=True,
    )
    short_description = models.TextField()
    description = HTMLField()
    details = HTMLField()
    created_time = models.DateTimeField(
        auto_now_add=True,
    )
    updated_time = models.DateTimeField(
        auto_now=True,
    )
    image = models.ImageField(
        upload_to='images/product/%Y/%m/%d',
        blank=False,
        null=False,
    )
    price = models.BigIntegerField(
        default=10_000,
    )
    rate = models.FloatField(
        default=5,
    )
    stock_count = models.PositiveIntegerField(
        default=10,
    )
    sales = models.PositiveIntegerField(
        default=0,
    )

    def get_rating(self):
        INCREASER = 0.2
        rate = round(self.rate+INCREASER, 1)
        stars = int(rate // 1)
        float_rate = round(rate - stars, 1)
        half_stars = int(float_rate // 0.5)
        empty_stars = int(5 - (stars + (half_stars / 2)))
        return stars, half_stars, empty_stars

    def get_absolute_url(self):
        return reverse('shop:product', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = self._random_slug(4)
            while Product.objects.filter(slug=slug).exists():
                slug = self._random_slug(4)
            self.slug = slug
        return super().save(*args, **kwargs)

    @staticmethod
    def _random_slug(length: int) -> str:
        return "".join(choices(ascii_letters, k=length))

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('-created_time',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        _("Images"),
        upload_to="images/product/%Y/%m/%d",
        blank=True,
    )

    def __str__(self) -> str:
        return self.image.url


class Order(models.Model):
    customer: User = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    order_time = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return f"{self.customer.username}'s order"

    class Meta:
        ordering = ('order_time',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        null=True,
        on_delete=models.SET_NULL,
    )
    product_price = models.IntegerField()
    product_count = models.PositiveIntegerField(
        default=1,
    )
    product_cost = models.IntegerField()

    def __str__(self) -> str:
        return f"order item {self.id}"

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')


class Invoice(models.Model):
    order = models.ForeignKey(
        Order,
        null=True,
        on_delete=models.SET_NULL,
    )
    invoice_time = models.DateTimeField(
        auto_now_add=True,
    )
    authority = models.CharField(
        max_length=36,
        blank=True,
        null=True,
        unique=True,
    )

    def __str__(self) -> str:
        return f"invoice {self.id}"

    class Meta:
        ordering = ('invoice_time',)
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')


class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = _('pending')
        FAILED = _('failed')
        COMPLETED = _('completed')

    invoice = models.ForeignKey(
        Invoice,
        null=True,
        on_delete=models.SET_NULL,
    )
    transaction_time = models.DateTimeField(
        auto_now_add=True,
    )
    amount = models.IntegerField()
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default='pending',
    )

    def __str__(self) -> str:
        return f"transaction {self.id}"

    class Meta:
        ordering = ('transaction_time',)
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
