from .serializers import (
    PriceThreeSerializer, FavouriteThreeModelSerializer, 
    FavouriteTwoModelSerializer, FavouriteDeleteSerializer,
    FavouriteTwoAllSerializer, FavouriteThreeAllSerializer, 
    PriceTwoSerializer, GetInfoBestChangeSerializer
)

from .models import FavouriteTwoModel, FavouriteThreeModel
from base.views import BaseFormView, BaseAPIView

from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import caches
from django.db import connections
from rest_framework import status


APP_NAME_URL = __package__ + '/'
ALL_EX = [
    'binance', 'bybit', 'huobi', 'kucoin', 'okx', 'bitget', 'pancake',
    'gateio'
]

class LinksWithoutCardsView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'links_without_cards.html'

class MezhbirzhevyeSvyazkiView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'mezhbirzhevye_svyazki.html'


class PriceViewThree(BaseAPIView):
    def get_serializer(self, data):
        return PriceThreeSerializer(data=data)

    def process_request(self, request, validated_data):
        def get_favorites(request):
            user = self.request.user
            favorites = FavouriteTwoModel.objects.filter(user=user)
            serializer = FavouriteTwoAllSerializer(favorites, many=True)
            return serializer.data

        market = validated_data.get('market')
        token = validated_data.get('token')

        key = f'{market}--{token}'
        data = caches['links_without_cards'].get(key)

        return {
            'data': data,
            'favourite': get_favorites(request),
        }

class PriceViewTwo(BaseAPIView):
    def get_serializer(self, data):
        return PriceTwoSerializer(data=data)

    def process_request(self, request, validated_data):
        def get_favorites(request):
            user = self.request.user
            favorites = FavouriteTwoModel.objects.filter(user=user)
            serializer = FavouriteTwoAllSerializer(favorites, many=True)
            return serializer.data

        def filter_exchanges(exs):
            return [ex for ex in ALL_EX if ex not in exs] if exs else ALL_EX

        def get_data(fil_ex_buy, fil_ex_sell, trade_type):
            def key(trade_type, ex_buy, ex_sell):
                return f'{trade_type}--{ex_buy}--{ex_sell}'

            cache = caches['links_without_cards']

            pairs = [(a, b) for a in fil_ex_buy for b in fil_ex_sell if a != b]
            values = [cache.get(key(trade_type, a, b)) for a, b in pairs]

            total_value = []
            for sublist in values:
                if sublist:
                    total_value.extend(sublist)
                    
            sorted_data = sorted(total_value, key=lambda item: item['spread'], reverse=True)
            return sorted_data

        exs_buy = validated_data.get('exchanges_buy')
        exs_sell = validated_data.get('exchanges_sell')
        trade_type = validated_data.get('trade_type') \
            .split('_')[1]

        fil_ex_buy = filter_exchanges(exs_buy)
        fil_ex_sell = filter_exchanges(exs_sell)

        data = get_data(fil_ex_buy, fil_ex_sell, trade_type)
        favourite = get_favorites(request)

        return {
            'data': data,
            'favourite': favourite,
        }


class FavouriteThreeView(APIView):
    def post(self, request):
        serializer = FavouriteThreeModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': 'success'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = FavouriteDeleteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                id = serializer.validated_data.get('id')
                instance = FavouriteThreeModel.objects.get(id=id)
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            except FavouriteThreeModel.DoesNotExist:
                return Response(
                    {'status': 'error', 'message': 'Object not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FavouriteTwoView(APIView):
    def post(self, request):
        serializer = FavouriteTwoModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': 'success'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = FavouriteDeleteSerializer(data=request.data)
        if serializer.is_valid():
            try:
                id = serializer.validated_data.get('id')
                instance = FavouriteTwoModel.objects.get(id=id)
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            except FavouriteTwoModel.DoesNotExist:
                return Response(
                    {'status': 'error', 'message': 'Object not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetInfoBestChange(BaseAPIView):
    def get_serializer(self, data):
        return GetInfoBestChangeSerializer(data=data)

    def process_request(self, request, validated_data):
        def get_data(id):
            with connections['links_without_cards'].cursor() as cursor:
                cursor.execute(
                    'SELECT '
                        'exchange_id, '
                        'exchange_name, '
                        'info_reverse, '
                        'info_age, '
                        'info_star, '
                        'info_verification, '
                        'info_registration, '
                        'addition_floating, '
                        'addition_verifying, '
                        'addition_manual, '
                        'addition_percent, '
                        'addition_otherin, '
                        'addition_reg '
                    'FROM links_exchange_info '
                    'WHERE exchange_id = %s;',
                    [id]
                )
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]

            return result

        id = validated_data.get('id')
        data = get_data(id)

        return data