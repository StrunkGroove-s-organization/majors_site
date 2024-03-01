import random
import string

from os import getenv

from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from functools import partial

from accounts.forms import User
from payment.forms import Subscription
from payment.models import Order, CompleteOrder

APP_NAME = __package__


class ProfileView(View):
    template_name = 'profile.html'

    @staticmethod
    def get_subscription_end_date(user) -> str:
        return user.subscription_end.strftime('%d.%m.%Y')
        
    @method_decorator(partial(login_required, login_url='/', redirect_field_name=None))
    def get(self, request, *args, **kwargs):
        user = request.user
        refferal = user.referral_info

        users = User.objects.filter(referral_belongs_to=refferal)
        orders = Order.objects.filter(referral=refferal)
        complete_orders = CompleteOrder.objects.filter(order__referral=refferal)

        return render(request, f'{APP_NAME}/{self.template_name}', {
            'referral': refferal,
            'invited_users': users if users else [],
            'payments': orders if orders else [],
            'complete_payments': complete_orders if complete_orders else [],

            'domain': getenv('DOMAIN'),
            'username': user.username,
            'email': user.email,
            'subscription_end': self.get_subscription_end_date(user),
            'type_subscription': user.type_subscription,
            'subscription': Subscription,
        })


