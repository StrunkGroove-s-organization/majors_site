from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.ReferralView.as_view(), name='ref-main'),
]
