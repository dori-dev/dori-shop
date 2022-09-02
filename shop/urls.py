from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('p/<slug:slug>/', views.product_detail, name='product'),
    path('store/', views.store, name='store'),
    path('checkout/', views.checkout, name='checkout'),
    path('to-bank/<int:order_id>/', views.to_bank, name='to_bank'),
    path('callback/', views.callback, name='callback'),
]
