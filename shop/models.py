from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='images/product/%Y/%m/%d',
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product', args=(self.id,))

    class Meta:
        ordering = ('created_time',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Order(models.Model):
    customer: User = models.ForeignKey(User, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.customer.username}'s order"

    class Meta:
        ordering = ('order_time',)
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    product_count = models.PositiveIntegerField(default=1)
    product_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self) -> str:
        return f"order item {self.id}"

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')


class Invoice(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    invoice_time = models.DateTimeField(auto_now_add=True)

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
    invoice = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL)
    transaction_time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default='pending'
    )

    def __str__(self) -> str:
        return f"transaction {self.id}"

    class Meta:
        ordering = ('transaction_time',)
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
