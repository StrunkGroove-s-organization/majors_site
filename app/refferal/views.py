import random
import string

from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from functools import partial

from .models import Referral


APP_NAME = __package__


class ReferralView(View):
    template_name = 'referral.html'

    def generate_referral_code(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    def create_referral(self, user):
        referral_code = self.generate_referral_code()
        referral = Referral.objects.create(user=user, referral_code=referral_code)
        return referral

    @method_decorator(partial(login_required, login_url='/', redirect_field_name=None))
    def get(self, request, *args, **kwargs):
        user = request.user
        referral = user.referral
        if referral:
            invited_users = referral.invited_users.all()
            payments = referral.payments.all()
            return render(request, f'{APP_NAME}/{self.template_name}', {
                'referral': referral, 
                'invited_users': invited_users, 
                'payments': payments
            })
        elif not referral:
            referral = self.create_referral(user)
            return render(request, f'{APP_NAME}/{self.template_name}', {
                'referral': referral
            })
