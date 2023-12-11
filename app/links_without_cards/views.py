import requests

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import FavouriteTwoModel, FavouriteThreeModel
from base.views import BaseFormView, BaseAPIView
from .serializers import (
    PriceThreeSerializer, FavouriteThreeModelSerializer, 
    FavouriteTwoModelSerializer, FavouriteDeleteSerializer,
    FavouriteTwoAllSerializer, FavouriteThreeAllSerializer, 
    PriceTwoSerializer, GetInfoBestChangeSerializer
)

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
        market = validated_data.get('market')
        token = validated_data.get('token')

        payload = {"market": market, "token": token}
        url = 'http://188.120.227.131:8001/api/v1/triangular-arbitrage/'
        response = requests.post(url, data=payload)
        return response.json()


class PriceViewTwo(BaseAPIView):
    def get_serializer(self, data):
        return PriceTwoSerializer(data=data)

    def process_request(self, request, validated_data):
        exs_buy = validated_data.get('exchanges_buy', [])
        exs_sell = validated_data.get('exchanges_sell', [])
        trade_type = validated_data.get('trade_type')

        payload = {"exchanges_buy": exs_buy,
                   "exchanges_sell": exs_sell, "trade_type": trade_type}
        url = 'http://188.120.227.131:8001/api/v1/inter-arbitrage/'
        response = requests.post(url, data=payload)
        return response.json()


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