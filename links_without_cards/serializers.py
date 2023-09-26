from rest_framework import serializers

class PriceThreeSerializer(serializers.Serializer):
    market = serializers.CharField()
    token = serializers.CharField()

    def validate_market(self, value):
        list = ['binance', 'bybit']
        if value not in list:
            raise serializers.ValidationError(f'Допустимые значения: {list}')
        return value

    def validate_token(self, value):
        list = ['USDT', 'BTC', 'BNB', 'TUSD']
        if value not in list:
            raise serializers.ValidationError(f'Допустимые значения: {list}')
        return value


class PriceTwoSerializer(serializers.Serializer):
    exchange_first = serializers.CharField()
    exchange_second = serializers.CharField()

    def validate_exchange_first(self, value):
        list = ['binance', 'bybit', 'hodlhodl', 'huobi', 'kucoin']
        if value not in list:
            raise serializers.ValidationError(f'Допустимые значения: {list}')
        return value

    def validate_exchange_second(self, value):
        list = ['binance', 'bybit', 'hodlhodl', 'huobi', 'kucoin']
        if value not in list:
            raise serializers.ValidationError(f'Допустимые значения: {list}')
        return value