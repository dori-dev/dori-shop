from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description', 'created_time',
        'updated_time', 'price'
    )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_time')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'order', 'product',
        'product_price', 'product_count', 'product_cost'
    )


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'invoice_time')


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'invoice', 'amount',
        'transaction_time', 'status'
    )


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)
admin.site.register(models.Transaction, TransactionAdmin)
