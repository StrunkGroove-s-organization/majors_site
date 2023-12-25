from rest_framework import serializers
from .models import (
    CryptoFilterModel, ExchangeFilterModel, PaymentsFilterModel, 
    TradeTypeFilterModel
)


class P2PCryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoFilterModel
        fields = ('name',)

class P2PExchangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeFilterModel
        fields = ('pk',)

class P2PPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentsFilterModel
        fields = ('pk',)

class P2PTradeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeTypeFilterModel
        fields = ('pk',)

class P2PFilterSerializer(serializers.Serializer):
    # crypto = P2PCryptoSerializer()
    # exchanges = P2PExchangesSerializer(many=True)
    # payment_methods = P2PPaymentsSerializer(many=True)

    crypto = serializers.CharField()
    exchanges = serializers.ListField(child=serializers.CharField())
    payment_methods = serializers.ListField(child=serializers.CharField())
    trade_type = serializers.CharField()

    def validate_trade_type(self, value):
        try:
            crypto_obj = TradeTypeFilterModel.objects.get(pk=value)
            return crypto_obj.name
        except TradeTypeFilterModel.DoesNotExist:
            raise serializers.ValidationError("Record doesn't exist.")

    def validate_crypto(self, value):
        try:
            crypto_obj = CryptoFilterModel.objects.get(pk=value)
            return crypto_obj.name
        except CryptoFilterModel.DoesNotExist:
            raise serializers.ValidationError("Record doesn't exist.")

    def validate_exchanges(self, value):
        names = ExchangeFilterModel.objects \
            .filter(pk__in=value) \
            .values_list('name', flat=True)

        if not names.exists():
            raise serializers.ValidationError("Records doesnt exist.")
        return list(names)

    def validate_payment_methods(self, value):
        names = PaymentsFilterModel.objects \
            .filter(pk__in=value) \
            .values_list('name', flat=True)

        if not names.exists():
            raise serializers.ValidationError("Records doesnt exist.")
        return list(names)

    ord_q = serializers.FloatField(required=False)
    ord_p = serializers.FloatField(required=False)
    lim_first = serializers.FloatField(required=False)
    lim_second = serializers.FloatField(required=False)
    user_spread = serializers.FloatField(required=False)
    available_first = serializers.FloatField(required=False)
    available_second = serializers.FloatField(required=False)
    only_stable_coin = serializers.BooleanField(required=False)

    def validate_ord_q(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Order quantity must be a non-negative number."
            )
        return value

    def validate_ord_p(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Order price must be a non-negative number."
            )
        return value

    def validate_user_spread(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Spread max must be a non-negative number."
            )
        return value

    def validate_lim_first(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Limit sell must be a non-negative number."
            )
        return value

    def validate_lim_second(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError(
                "Limit buy must be a non-negative number."
            )
        return value

    def validate_available_first(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Available rub buy must be a non-negative number."
            )
        return value

    def validate_available_second(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Available rub sell must be a non-negative number."
            )
        return value

    def validate_only_stable_coin(self, value):
        if value not in [True, False]:
            raise serializers.ValidationError(
                "Only stable coin in True or False"
            )
        return value