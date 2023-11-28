from django.urls import path
from . import views

urlpatterns = [
    path('p2pprices/', views.P2PPricesView.as_view(), name='p2pprices'),
    path('best_prices/', views.BestPricesView.as_view(), name='best_prices'),
    path('api/best_prices/', views.PriceView.as_view()),
]