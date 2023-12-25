from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from payment.forms import Subscription

@login_required(login_url='/', redirect_field_name=None)
def profile_view(request):
    user_profile = request.user

    subscription_end_date = user_profile.subscription_end
    context = {
        'username': user_profile.username,
        'email': user_profile.email,
        'subscription_end': subscription_end_date.strftime('%d.%m.%Y'),
        'type_subscription': user_profile.type_subscription,
        'subscription': Subscription,
    }

    return render(request, 'user_profile/profile.html', context)
