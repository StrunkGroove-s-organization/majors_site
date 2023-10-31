from .serializers import PriceSerializer
# from .services import get_best_prices_objects
from base.views import BaseFormView, BaseAPIView

from django.core.cache import caches


APP_NAME_URL = __package__ + '/'


class P2PPricesView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'p2pprices.html'

class BestPricesView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'best_prices.html'


class PriceView(BaseAPIView):
    def get_serializer(self, data):
        return PriceSerializer(data=data)

    def process_request(self, request, validated_data):
        token = validated_data.get('token')
        site = validated_data.get('buy_sell')

        key = f'{site}--{token}'
        value = caches['p2p_server'].get(key)

        return value