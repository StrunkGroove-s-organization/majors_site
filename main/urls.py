from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('empty/', views.EmptyView.as_view(), name='empty'),
]
