from .serializers import PriceThreeSerializer, PriceTwoSerializer
from base.views import BaseFormView, BaseAPIView

from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import caches

# from django.core.cache import caches


APP_NAME_URL = __package__ + '/'


class LinksWithoutCardsView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'links_without_cards.html'

class MezhbirzhevyeSvyazkiView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'mezhbirzhevye_svyazki.html'


class PriceViewThree(BaseAPIView):
    def get_serializer(self, data):
        return PriceThreeSerializer(data=data)

    def process_request(self, validated_data):
        market = validated_data.get('market')
        token = validated_data.get('token')

        key = f'{market}--{token}'
        value = caches['links_without_cards'].get(key)

        return value

class PriceViewTwo(APIView):
    def post(self, request):
        cache = caches['links_without_cards']
        value = cache.get('huobi--bybit')
        value += cache.get('bybit--huobi')
        value += cache.get('binance--huobi')
        value += cache.get('binance--bybit')
        value += cache.get('huobi--binance')
        value += cache.get('bybit--binance')
        value += cache.get('kucoin--binance')
        value += cache.get('kucoin--bybit')
        value += cache.get('kucoin--huobi')
        value += cache.get('binance--kucoin')
        value += cache.get('bybit--kucoin')
        value += cache.get('huobi--kucoin')

        value += cache.get('okx--huobi')
        value += cache.get('okx--bybit')
        value += cache.get('okx--binance')
        value += cache.get('okx--kucoin')
        value += cache.get('huobi--okx')
        value += cache.get('bybit--okx')
        value += cache.get('binance--okx')
        value += cache.get('kucoin--okx')

        return Response(value)

# class PriceViewTwo(BaseAPIView):
#     def get_serializer(self, data):
#         return PriceTwoSerializer(data=data)

#     def process_request(self, validated_data):
#         exchange_first = validated_data.get('exchange_first')
#         exchange_second = validated_data.get('exchange_second')

#         key = f'{exchange_first}--{exchange_second}'
#         value = caches['links_without_cards'].get(key)

#         return value