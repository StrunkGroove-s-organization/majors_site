import random
import string

from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from functools import partial

from refferal.models import Referral
from payment.forms import Subscription


APP_NAME = __package__


class ReferralView(View):
    template_name = 'profile.html'

    def generate_referral_code(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    def create_referral(self, user):
        referral_code = self.generate_referral_code()
        referral = Referral.objects.create(user=user, referral_code=referral_code)
        return referral

    def get_subscription_end_date(self, user):
        return user.subscription_end.strftime('%d.%m.%Y')

    def get_user_referral(self, user):
        try:
            return user.referral
        except Referral.DoesNotExist:
            return self.create_referral(user)
        
    @method_decorator(partial(login_required, login_url='/', redirect_field_name=None))
    def get(self, request, *args, **kwargs):
        user = request.user

        referral = self.get_user_referral(user)

        return render(request, f'{APP_NAME}/{self.template_name}', {
            'referral': referral,
            'invited_users': referral.invited_users.all() if referral else [],
            'payments': referral.payments.all() if referral else [],
            'complete_payments': referral.complete_payments.all() if referral else [],

            'username': user.username,
            'email': user.email,
            'subscription_end': self.get_subscription_end_date(user),
            'type_subscription': user.type_subscription,
            'subscription': Subscription,
        })


