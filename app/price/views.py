import requests

from django.core.cache import caches

from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import PriceSerializer
from base.views import BaseFormView, BaseAPIView


APP_NAME_URL = __package__ + '/'


class P2PPricesView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'p2pprices.html'


class BestPricesView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'best_prices.html'


class PriceView(BaseAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PriceSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        url = 'http://188.120.227.131:8001/api/v1/best-prices/'
        response = requests.post(url, json=serializer.validated_data)
        return Response({'data': response.json()})
    

    def process_request(self, request, validated_data):
        token = validated_data.get('token')
        site = validated_data.get('buy_sell')

        key = f'{site}--{token}'
        value = caches['p2p_server'].get(key)

        return value