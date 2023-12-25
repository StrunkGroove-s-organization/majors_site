from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseRedirect

from .models import Referral


class ReferralMiddleware(MiddlewareMixin):
    def process_request(self, request):
        referral_code = request.GET.get('ref')

        if referral_code:
            request.session['referral_code'] = referral_code
            
            new_url = request.path
            query_params = request.GET.copy()
            del query_params['ref']
            if query_params:
                new_url += '?' + query_params.urlencode()

            referral, created = Referral.objects.get_or_create(referral_code=referral_code)
            referral.increment_clicks()

            return HttpResponseRedirect(new_url)

