from django.urls import path

from . import views

app_name = 'comment'
urlpatterns = [
    path(
        'product-comment/<int:pk>/',
        views.send_product_comment,
        name='product',
    ),
]
