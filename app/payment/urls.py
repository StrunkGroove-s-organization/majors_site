from django.urls import path, include
from . import views

urlpatterns = [
    path('payment_crypto/', views.create_payment_plisio, name='payment_crypto'),
    path('payment_fiat/', views.payment_fiat, name='payment_fiat'),
    path('paymenterror/', views.paymenterror, name='paymenterror'),
    path('payment_success/', views.payment_success, name='payment_success'),
]
