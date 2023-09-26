from django.urls import path
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
     path('custom_logout/', views.custom_logout, name='custom_logout'),
     path('registration/', views.reg_view, name='registration'),
     path('login/', views.login_view, name='login'),
]
