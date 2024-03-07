from django.urls import path
from .views import CreatePaymentPlisio, PaymentError, PaymentSuccess

urlpatterns = [
    path('payment_crypto/', CreatePaymentPlisio.as_view(), name='payment_crypto'),
    path('paymenterror/', PaymentError.as_view(), name='paymenterror'),
    path('payment_success/', PaymentSuccess.as_view(), name='payment_success'),
]
