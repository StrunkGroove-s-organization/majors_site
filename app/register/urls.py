from django.urls import path
from . import views


app_name = 'register'


urlpatterns = [
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),

]
