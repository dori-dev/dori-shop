from datetime import datetime

from django.contrib import admin
from django.utils.html import format_html

from . import models
from shop.models import Product


@admin.action(description='Confirm selected product comments')
def confirm_product_comments(modeladmin, request, queryset):
    queryset.update(confirmed=True)


@admin.action(description='Un confirm selected product comments')
def un_confirm_product_comments(modeladmin, request, queryset):
    queryset.update(confirmed=False)


@admin.register(models.ProductComment)
class AdminProductComment(admin.ModelAdmin):
    fieldsets = [
        (
            None, {
                'fields': [
                    'user',
                    'product',
                ]
            }
        ),
        (
            'Details', {
                'fields': [
                    'body',
                    'rate',
                ]
            }
        ),
        (
            'Confirmation', {
                'fields': [
                    'confirmed',
                ]
            }
        ),
    ]
    list_display = (
        'user',
        'product_',
        'rate',
        'send_at_',
        'confirmed',
    )

    list_filter = (
        'confirmed',
    )
    search_fields = (
        'user__username',
        'user__firstname',
        'user__lastname',
        'email',
        'body',
    )
    raw_id_fields = (
        'user',
        'product',
    )
    actions = (
        confirm_product_comments,
        un_confirm_product_comments,
    )
    date_hierarchy = 'send_at'

    def product_(self, model: models.ProductComment):
        product: Product = model.product
        url = product.get_absolute_url()
        return format_html(f'<a target="_blank" href="{url}">Link</a>')

    def send_at_(self, model: models.ProductComment):
        send_time: datetime = model.send_at
        return send_time.strftime('%b %d, %I:%M %p')
