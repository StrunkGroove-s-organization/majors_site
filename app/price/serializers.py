from rest_framework import serializers


class PriceSerializer(serializers.Serializer):
    BUY_SELL_CHOICES = ['BUY', 'SELL']
    TOKEN_CHOICES = [
        'USDT', 'BTC', 'ETH', 'BUSD', 'BNB', 'DOGE', 'TRX', 'USDD', 'USDC', 
        'RUB', 'HT', 'EOS', 'XRP', 'LTC', 'GMT', 'TON', 'XMR', 'DAI', 'TUSD'
    ]

    token = serializers.ChoiceField(
        choices=TOKEN_CHOICES, required=True
    )
    buy_sell = serializers.ChoiceField(
        choices=BUY_SELL_CHOICES, required=True
    )
