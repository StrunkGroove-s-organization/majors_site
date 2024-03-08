from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('empty/', views.EmptyView.as_view(), name='empty'),
    path('cookies/', views.Cookies.as_view(), name='cookies'),
    path('privacy-policy/', views.PrivacyPolicy.as_view(), name='privacy_policy'),
    path('terms-of-use/', views.TermsOfUse.as_view(), name='terms_of_use'),
    path(
        'denial-of-responsibility/', 
        views.DenialOfResponsibility.as_view(), 
        name='denial_of_responsibility'
    ),
    path(
        'calculator_spread/', 
        views.CalculatorSpread.as_view(), 
        name='calculator_spread'
    ),
]