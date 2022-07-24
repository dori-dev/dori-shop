from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('product', views.product, name='index'),
    path('store', views.store, name='index'),
    path('checkout', views.checkout, name='index')
]
