from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from payment.forms import Subscription

@login_required(login_url='/')
def profile_view(request):
    user_profile = request.user

    context = {
        'username': user_profile.username,
        'email': user_profile.email,
        'subscription_end': user_profile.subscription_end,
        'type_subscription': user_profile.type_subscription,
        'subscription': Subscription,
    }

    return render(request, 'user_profile/profile.html', context)
