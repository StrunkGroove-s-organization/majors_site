from django.urls import path
from . import views

app_name = 'register'


urlpatterns = [
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('accounts/reset/<uidb64>/<token>/', views.CustomPasswordResetView.as_view(), name ='password_reset_confirm'),
    path('accounts/reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
]
