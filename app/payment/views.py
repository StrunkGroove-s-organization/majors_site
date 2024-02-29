import os
import cgi
import io
import secrets
import logging
import requests

from datetime import timedelta, datetime, timezone

from .models import Order, CompleteOrder
from .forms import Subscription
from .tasks import send_gratitude_for_payment
from refferal.models import Referral
from accounts.forms import User

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


API_KEY = os.getenv('API_ADM')
URL = os.getenv('URL_PLISIO')

logger = logging.getLogger(__name__)


def generate_token(length=15):
    allowed_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(secrets.choice(allowed_chars) for _ in range(length))

@login_required(login_url='/')
def create_payment_plisio(request):
    if request.method == 'POST':
        filters = Subscription(request.POST)
        if filters.is_valid():
            user_profile = request.user

            selected_subscription = filters.cleaned_data['subscription'].split('_')
            currency = filters.cleaned_data['currency']

            days = int(selected_subscription[0])
            type_sub = selected_subscription[1]
            amount = int(selected_subscription[2])
            if type_sub == 'test' and currency == 'USDT_BSC':
                amount = 3
            email = user_profile.email
            token = generate_token()

            params = {
                "source_currency": 'USD',
                "source_amount": amount,
                "order_number": token,
                "currency": currency,
                "email": email,
                "order_name": type_sub,
                "api_key": API_KEY,
                "json": True,
            }

            order = Order.objects.create(email=email,
                                         type=type_sub,
                                         days=days,
                                         token=token,
                                         amount=amount
                                         )

            response = requests.get(URL, params=params)
            res_data = response.json()
            
            if res_data.get("status") == 'success':
                # Refferal system
                try:
                    referral_instance = Referral.objects.get(invited_users=user_profile)
                    referral_instance.payments.add(order)
                except Referral.DoesNotExist:
                    referral_instance = None

                # Payment
                data = res_data.get("data")

                image_data = data.get("qr_code")
                pay_url = data.get('invoice_url')
                currency = data.get('currency')
                invoice_total_sum = data.get('invoice_total_sum')
                wallet_hash = data.get('wallet_hash')

                response_data = {
                    'pay_url': pay_url,
                    'currency': currency,
                    'wallet_hash': wallet_hash,
                    'image': image_data,
                    'sum': invoice_total_sum,
                }
                return JsonResponse(response_data)
        
    error_data = {
        'error': 'An error occurred',
        'message': 'Error method',
    }
    return JsonResponse(error_data, status=400)


@login_required(login_url='/')
def payment_fiat(request):
    if request.method == 'POST':
        response_data = {
            'pay_url': 'https://google.com',
        }
        return JsonResponse(response_data)

    else:
        error_data = {
            'error': 'Произошла ошибка',
            'message': 'Подробное описание ошибки здесь...',
        }
        return JsonResponse(error_data, status=400)


@login_required(login_url='/')
def paymenterror(request):
    return HttpResponse('Ошибка во время оплаты.')


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        stream = io.BytesIO(body.encode())
        content_type = request.META.get('CONTENT_TYPE', '')
        boundary = content_type.split('; ')[1].split('=')[1]
        params = {'boundary': boundary.encode('utf-8')}
        list_response = cgi.parse_multipart(stream, params)
        status = list_response.get('status')[0]

        if status == 'new' \
        or status == 'cancelled' \
        or status == 'error' \
        or status == 'expired' \
        or status == 'pending internal' \
        or status == 'pending':
            return JsonResponse({'status': 'not completed'})

        elif status == 'completed' or status == 'mismatch':

            token = list_response.get('order_number')[0]
            type = list_response.get('order_name')[0]
            currency = list_response.get('currency')[0]
            amount = list_response.get('amount')[0]

            try:
                order = Order.objects.get(token=token)
            except Order.DoesNotExist as e:
                return JsonResponse({'error': e})

            email = order.email
            days = order.days

            complete_order = CompleteOrder.objects.create(
                email=email,
                type=type,
                days=days,
                token=token,
                currency=currency,
                amount_crypto=amount,
            )

            # send_gratitude_for_payment.delay(email)

            user = User.objects.get(email=email)

            # Refferal system
            try:
                referral_instance = Referral.objects.get(invited_users=user)
                referral_instance.complete_payments.add(complete_order)
            except Referral.DoesNotExist:
                pass

            if type == 'infinity':
                user.has_infinity_subscription = True
                user.type_subscription = type

            elif type != 'infinity':
                now = datetime.now(timezone.utc)
                end = user.subscription_end 

                if end > now:
                    left_sub = end - now
                    user.subscription_end = now + left_sub + timedelta(days=days)
                    user.type_subscription = type
                    
                elif end <= now:  
                    user.subscription_start = now
                    user.subscription_end = now + timedelta(days=days)
                    user.type_subscription = type
            user.save()

        else:
            pass

    return JsonResponse({})
