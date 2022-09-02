from datetime import datetime

from django.contrib import admin
from django.utils.html import format_html

from . import models


class ProductImageAdmin(admin.TabularInline):
    model = models.ProductImage


class PriceFilter(admin.SimpleListFilter):
    title = 'Price'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('cheap', 'less than 100,000'),
            ('normal', 'less than 1,000,000'),
            ('expensive', 'greater than 1,000,000')
        )

    def queryset(self, request, queryset):
        if self.value() == 'cheap':
            return queryset.filter(
                price__lt=100_000,
            )
        if self.value() == 'normal':
            return queryset.filter(
                price__range=(100_000, 1_000_000),
            )
        if self.value() == 'expensive':
            return queryset.filter(
                price__gt=1_000_000,
            )


class StockFilter(admin.SimpleListFilter):
    title = 'Stock Count'
    parameter_name = 'stock'

    def lookups(self, request, model_admin):
        return (
            ('unavailable', 'zero stock'),
            ('less', 'less than 10 stock'),
            ('available', 'greater than 10')
        )

    def queryset(self, request, queryset):
        if self.value() == 'unavailable':
            return queryset.filter(
                stock_count=0,
            )
        if self.value() == 'less':
            return queryset.filter(
                stock_count__lte=10,
            )
        if self.value() == 'available':
            return queryset.filter(
                stock_count__gt=10,
            )


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'name',
                ]
            }
        ),
        (
            'Description', {
                'fields': [
                    'short_description',
                    'description',
                    'details',
                ]
            }
        ),
        (
            'Image', {
                'fields': [
                    'image',
                ]
            }
        ),
        (
            'Information', {
                'fields': [
                    'price',
                    'rate',
                    'stock_count',
                ]
            }
        )
    ]
    list_display = (
        'name',
        'link',
        'create_at',
        'update_at',
        'image_',
        'price_',
        'rate',
        'stock_count',
    )

    list_filter = (
        # 'category',
        PriceFilter,
        StockFilter,
    )
    search_fields = (
        'name',
        'short_description',
        'description',
        'details',
    )
    date_hierarchy = 'created_time'

    inlines = (ProductImageAdmin,)

    def link(self, model: models.Product):
        url = model.get_absolute_url()
        return format_html(f'<a target="_blank" href="{url}">Link</a>')

    def image_(self, model: models.Product):
        image_url = model.image.url
        return format_html(f'<a target="_blank" href="{image_url}">Image</a>')

    def price_(self, model: models.Product):
        price = model.price
        return f"{price:,}"

    def create_at(self, model: models.Product):
        created_time: datetime = model.created_time
        return created_time.strftime('%b %d, %I:%M %p')

    def update_at(self, model: models.Product):
        updated_time: datetime = model.updated_time
        return updated_time.strftime('%b %d, %I:%M %p')


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
