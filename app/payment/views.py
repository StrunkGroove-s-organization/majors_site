import json
import cgi
import io
import secrets
import logging
import base64

import requests
import base64
from PIL import Image
from io import BytesIO
from datetime import timedelta
from datetime import datetime, timezone

from .models import Order, CompleteOrder
from .forms import Subscription
from .tasks import send_gratitude_for_payment
from accounts.forms import User

from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

# API_KEY = "LnFZ4XHmg4lgUbPCrLfnTir--tcJh0EAYQjfMJnD8m0LlxkSn2MMYv4-3qp0YXvx"
API_KEY = "JupTf7vo8MMWBWbyO4LA4ALzbinbQTaU28LdJjsd4zzKS9KCqUVRPoEEuUXlNPyJ"

URL = "https://plisio.net/api/v1/invoices/new"

ALLOWED_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

logger = logging.getLogger(__name__)


def generate_token(length=15):
    allowed_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(secrets.choice(allowed_chars) for _ in range(length))


# class PaymentPlisioView(View):
#     def post(self, request):
#         filters = Subscription(request.POST)
#         if filters.is_valid():
#             user_profile = request.user

#             selected_subscription = filters.cleaned_data['subscription'].split('_')
#             currency = filters.cleaned_data['currency']

#             days = int(selected_subscription[0])
#             type_sub = selected_subscription[1]
#             amount = int(selected_subscription[2])
#             email = user_profile.email
#             token = generate_token()

#             params = {
#                 "source_currency": 'USD',
#                 "source_amount": amount,
#                 "order_number": token,
#                 "currency": currency,
#                 "email": email,
#                 "order_name": type_sub,
#                 "api_key": API_KEY,
#                 "json": True,
#             }

#             Order.objects.create(
#                 email=email,
#                 type=type_sub,
#                 days=days,
#                 token=token,
#                 amount=amount
#             )

#             response = requests.get(URL, params=params)
#             data = response.json()
            
#             if data.get("status") == 'success':
#                 data = data.get("data")
#                 response_data = {
#                     'pay_url': data.get('invoice_url'),
#                     'currency': data.get('currency'),
#                     'wallet_hash': data.get('wallet_hash'),
#                     'image': data.get("qr_code"),
#                     'sum': data.get('invoice_total_sum'),
#                 }
#                 return JsonResponse(response_data)
#         error_data = {
#             'error': 'An error occurred',
#             'message': 'Error method',
#         }
#         return JsonResponse(error_data, status=400)



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

            Order.objects.create(email=email, type=type_sub, days=days, token=token, amount=amount)

            response = requests.get(URL, params=params)
            data = response.json()
            print(data)
            
            if data.get("status") == 'success':
                data = data.get("data")

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
            except:
                return JsonResponse({})

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

            send_gratitude_for_payment.delay(email)
            
            user = User.objects.get(email=email)
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