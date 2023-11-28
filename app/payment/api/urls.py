from django.urls import path, include
from . import views

urlpatterns = [
    path('payment/', views.PaymentPlisio.as_view()),
]
