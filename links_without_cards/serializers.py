from rest_framework import serializers
from accounts.models import User
from .models import (
    FavouriteThreeModel, FavouriteTwoModel
)


class PriceThreeSerializer(serializers.Serializer):
    market = serializers.CharField()
    token = serializers.CharField()

    def validate_market(self, value):
        list = ['binance', 'bybit', 'huobi', 'kucoin', 'okx']
        if value not in list:
            raise serializers.ValidationError(f'Допустимые значения: {list}')
        return value

    def validate_token(self, value):
        list = ['USDT', 'USDC']
        if value not in list:
            raise serializers.ValidationError(f'Допустимые значения: {list}')
        return value

class PriceTwoSerializer(serializers.Serializer):
    exchanges_buy = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    exchanges_sell = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    trade_type = serializers.CharField()

    def validate_trade_type(self, value):
        valid_list = [
            'T-T_BUY-SELL', 'T-M_BUY-BUY', 'M-T_SELL-SELL', 'M-M_SELL-BUY'
        ]
        if value not in valid_list:
            raise serializers.ValidationError(f'Invalid exchange: {value}')
        return value
    
    def validate_exchanges_buy(self, value):
        valid_exchanges = [
            'binance', 'bybit', 'huobi', 'kucoin', 'okx', 'bitget',
            'pancake', 'gateio'
        ]
        for exchange in value:
            if exchange not in valid_exchanges:
                raise serializers.ValidationError(
                    f'Invalid exchange: {exchange}'
                )
        return value
    
    def validate_exchanges_sell(self, value):
        valid_exchanges = [
            'binance', 'bybit', 'huobi', 'kucoin', 'okx', 'bitget',
            'pancake', 'gateio'
        ]
        for exchange in value:
            if exchange not in valid_exchanges:
                raise serializers.ValidationError(
                    f'Invalid exchange: {exchange}'
                )
        return value


class FavouriteTwoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteTwoModel
        fields = [
            'first_exchange', 'second_exchange', 'first_give', 'first_get', 'second_give', 'second_get'
        ]

    def validate_first_exchange(self, value):
        allowed_values = ['binance', 'bybit', 'huobi', 'kucoin']
        if value not in allowed_values:
            raise serializers.ValidationError(
                f'Допустимые значения: {allowed_values}'
            )
        return value

    def validate_second_exchange(self, value):
        allowed_values = ['binance', 'bybit', 'huobi', 'kucoin']
        if value not in allowed_values:
            raise serializers.ValidationError(
                f'Допустимые значения: {allowed_values}'
            )
        return value

    def validate_first_give(self, value):
        return value

    def validate_first_get(self, value):
        return value

    def validate_second_give(self, value):
        return value

    def validate_second_get(self, value):
        return value
    
    def create(self, validated_data):
        user = validated_data.pop('user')
        return FavouriteThreeModel.objects.create(user=user, **validated_data)

class FavouriteThreeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteThreeModel
        fields = [
            'base_crypto', 'exchange', 'best_change_exchange',
            'id_best_change_give', 'id_best_change_get'
        ]

    def validate_exchange(self, value):
        allowed_values = ['binance', 'bybit', 'huobi', 'kucoin']
        if value not in allowed_values:
            raise serializers.ValidationError(
                f'Допустимые значения: {allowed_values}'
            )
        return value

    def validate_base_crypto(self, value):
        allowed_values = ['USDT', 'USDC']
        if value not in allowed_values:
            raise serializers.ValidationError(
                f'Допустимые значения: {allowed_values}'
            )
        return value

    def validate_best_change_exchange(self, value):
        return value

    def validate_id_best_change_give(self, value):
        return value

    def validate_id_best_change_get(self, value):
        return value

    def create(self, validated_data):
        user = validated_data.pop('user')
        return FavouriteThreeModel.objects.create(user=user, **validated_data)

class FavouriteDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate_id(self, value):
        return value
    

class FavouriteThreeAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteThreeModel
        fields = [
            'base_crypto', 'exchange', 'best_change_exchange',
            'id_best_change_give', 'id_best_change_get', 'id'
        ]

class FavouriteTwoAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteTwoModel
        fields = '__all__'
