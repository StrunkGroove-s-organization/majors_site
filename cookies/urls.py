from django.urls import path
from . import views

urlpatterns = [
    path('cookies/', views.СookiesView.as_view(), name='cookies'),
]
