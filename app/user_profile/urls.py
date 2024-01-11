from django.urls import path, include
from . import views

urlpatterns = [
    path('profile/', views.ReferralView.as_view(), name='profile'),
]
