from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('main.urls')),
    path('', include('price.urls')),
    path('', include('p2plinks.urls')),
    path('', include('accounts.urls')),
    path('', include('user_profile.urls')),
    path('', include('blog.urls')),
    path('', include('payment.urls')),
    path('', include('register.urls')),
    path('', include('links_without_cards.urls')),

    path('api/', include('payment.api.urls')),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
