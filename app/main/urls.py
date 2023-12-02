from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('empty/', views.EmptyView.as_view(), name='empty'),
    path('cookies/', views.Cookies.as_view(), name='cookies'),
    path('calculator_spread/', views.CalculatorSpread.as_view(), name='calculator_spread'),
    path('test/', views.TestView.as_view(), name='test')
]