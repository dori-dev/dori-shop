"""config URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('cart/', include('cart.urls')),
    # path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('comment/', include('comments.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
