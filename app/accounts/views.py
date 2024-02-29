from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate

from .forms import CustomUserRegistrationForm, LoginForm
from .models import User
from refferal.models import Referral


def custom_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def reg_view(request):
    if request.method == 'POST':
        register_form = CustomUserRegistrationForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user = User.objects.create_user(username=username,
                                            email=email, 
                                            password=password
                                            )
            
            if user:
                login(request, user)

                referral_code = request.session.get('referral_code')
                if referral_code:
                    try:
                        referral = Referral.objects.get(referral_code=referral_code)
                        referral.invited_users.add(user)
                    except Referral.DoesNotExist:
                        pass
            return redirect(request.META.get('HTTP_REFERER', 'index'))
        else:
            errors = register_form.errors
        return JsonResponse(errors, status=400, safe=False)
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
            return redirect(request.META.get('HTTP_REFERER', 'index'))
        else:
            errors = login_form.errors
            return JsonResponse(errors, status=400, safe=False)
    return redirect('index')
