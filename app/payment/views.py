import cgi
import io
import logging
import uuid
from os import getenv
from datetime import datetime, timedelta, timezone

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order, CompleteOrder
from .forms import Subscription
from .tasks import send_gratitude_for_payment
from .schemas import PaymentData, SubscriptionData


API_KEY = getenv('API_ADM')
URL = getenv('URL_PLISIO')


logger = logging.getLogger(__name__)


class CreatePaymentPlisio(APIView):
    def post(self, request):
        filters = Subscription(request.POST)

        if not filters.is_valid():
            return Response({
                'message': 'Filters is not valid'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        subscription_data = self.__process_subscription_data(filters)

        user = request.user

        order = Order.objects.create(
            user=user,
            type=subscription_data.type_sub,
            days=subscription_data.days,
            token=f'{user.email}--{uuid.uuid4()}',
            amount=subscription_data.amount,
            currency=subscription_data.currency,
        )

        params = {
            "source_currency": 'USD',
            "source_amount": subscription_data.amount,
            "order_number": order.token,
            "currency": subscription_data.currency,
            "email": user.email,
            "order_name": subscription_data.type_sub,
            "api_key": API_KEY,
            "json": True,
        }

        response_json = self.__request_data_payment(params)
        
        if response_json.get("status") != 'success':
            return Response({
                'message': 'Cant get payment info.',
            }, status=status.HTTP_400_BAD_REQUEST)

        if user.referral_belongs_to:
            order.referral = user.referral_belongs_to
            order.save()

        response_data = response_json.get("data")

        return Response({
            'pay_url': response_data.get('invoice_url'),
            'currency': response_data.get('currency'),
            'wallet_hash': response_data.get('wallet_hash'),
            'image': response_data.get("qr_code"),
            'sum': response_data.get('invoice_total_sum'),
        }, status=status.HTTP_200_OK)

    @staticmethod
    def __request_data_payment(params):
        response = requests.get(URL, params=params)
        response.raise_for_status()
        return  response.json()
    
    @staticmethod
    def __process_subscription_data(filters) -> SubscriptionData:
        selected_subscription = filters.cleaned_data['subscription'].split('_')
        currency = filters.cleaned_data['currency']
        
        type_sub = selected_subscription[1]
        amount = selected_subscription[2]
        
        if type_sub == 'test' and currency == 'USDT_BSC':
            amount = 3
        
        return SubscriptionData(
            type_sub=type_sub, 
            days=selected_subscription[0], 
            amount=amount, 
            currency=currency
        )


class PaymentError(APIView):
    def get(self, request):
        return Response({
            'message': 'Error in payment.',
        }, status=status.HTTP_200_OK)


class PaymentSuccess(APIView):
    def post(self, request):
        response_status, list_response = self.parse_multipart_data(request)
        
        if response_status in ['new', 'cancelled', 'error', 'expired', 'pending internal', 'pending']:
            return Response({
                'status': 'not completed'
            }, status=status.HTTP_200_OK)
        
        elif response_status in ['completed', 'mismatch']:
            data = PaymentData(
                token=list_response.get('order_number')[0],
                type_subscription=list_response.get('order_name')[0],
                currency=list_response.get('currency')[0],
                amount=list_response.get('amount')[0],
            )
            self.handle_completed_status(data)
            return Response({}, status=status.HTTP_200_OK)
        
        return Response({
            'message: Oooops we are repairing it!. Sorry us for mistake :('
        }, status=status.HTTP_400_BAD_REQUEST)


    @staticmethod
    def parse_multipart_data(request):
        body = request.body.decode('utf-8')
        stream = io.BytesIO(body.encode())
        content_type = request.META.get('CONTENT_TYPE', '')
        boundary = content_type.split('; ')[1].split('=')[1]
        params = {'boundary': boundary.encode('utf-8')}
        list_response = cgi.parse_multipart(stream, params)
        status = list_response.get('status')[0]
        return status, list_response

    @staticmethod
    def handle_completed_status(data: PaymentData):
        try:
            order = Order.objects.get(token=data.token)
        except Order.DoesNotExist as e:
            raise Exception("Order not found.")

        CompleteOrder.objects.create(order=order)
        send_gratitude_for_payment.delay(order.user.email)
        user = order.user

        if data.type_subscription == 'infinity':
            user.has_infinity_subscription = True
        elif data.type_subscription != 'infinity':
            now = datetime.now(timezone.utc)
            end = user.subscription_end 

            if end > now:
                left_sub = end - now
                user.subscription_end = now + left_sub + timedelta(days=order.days) 
            elif end <= now:  
                user.subscription_start = now
                user.subscription_end = now + timedelta(days=order.days)
            
        user.type_subscription = data.type_subscription
        user.save()
