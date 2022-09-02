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


class SalesFilter(admin.SimpleListFilter):
    title = 'Sales'
    parameter_name = 'sales'

    def lookups(self, request, model_admin):
        return (
            ('low', 'less than 50 sales'),
            ('normal', 'less than 1000 sales'),
            ('many', 'greater than 1000 sales')
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(
                sales__lt=50,
            )
        if self.value() == 'normal':
            return queryset.filter(
                sales__range=(50, 1000),
            )
        if self.value() == 'many':
            return queryset.filter(
                sales__gt=1000,
            )


@admin.register(models.Product)
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
                    'sales',
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
        'sales',
        'stock_count',
    )

    list_filter = (
        # 'category',
        PriceFilter,
        SalesFilter,
        StockFilter,
    )
    search_fields = (
        'name',
        'short_description',
        'description',
        'details',
    )
    date_hierarchy = 'updated_time'
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


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'order_time',
    )


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'product_price',
        'product_count',
        'product_cost',
    )


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'invoice_time',
    )


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'invoice',
        'amount',
        'transaction_time',
        'status',
    )
