
from django import forms
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.forms import ModelForm

from .models import (
    CryptoFilterModel, ExchangeFilterModel, PaymentsFilterModel,
    TradeTypeFilterModel,
)

TRADE_TYPE_CHOICES = [
    ('M-M_SELL-BUY', 'Maker - Maker'),
    ('M-T_SELL-SELL', 'Maker - Taker'),
    ('T-M_BUY-BUY', 'Taker - Maker'),
    ('T-T_BUY-SELL', 'Taker - Taker'),
]

CRYPTO_CHOICES = [
    ('USDT', 'USDT'),
    ('BTC', 'BTC'),
    ('ETH', 'ETH'),
    # ('BUSD', 'BUSD'),
    # ('BNB', 'BNB'),
    # ('DOGE', 'DOGE'),
    # ('TRX', 'TRX'),
    # ('USDD', 'USDD'),
    ('USDC', 'USDC'),
    # ('RUB', 'RUB'),
    # ('HT', 'HT'),
    # ('EOS', 'EOS'),
    # ('XRP', 'XRP'),
    # ('LTC', 'LTC'),
    # ('GMT', 'GMT'),
    ('TON', 'TON'),
    ('XMR', 'XMR'),
    ('DAI', 'DAI'),
    # ('TUSD', 'TUSD'),
]

CRYPTO_CHOICES_V2 = [
    ('BTC', 'BTC'),
    ('ETH', 'ETH'),
    # ('BUSD', 'BUSD'),
    # ('BNB', 'BNB'),
    # ('DOGE', 'DOGE'),
    # ('TRX', 'TRX'),
    # ('USDD', 'USDD'),
    ('USDC', 'USDC'),
    # ('RUB', 'RUB'),
    # ('HT', 'HT'),
    # ('EOS', 'EOS'),
    # ('XRP', 'XRP'),
    # ('LTC', 'LTC'),
    # ('GMT', 'GMT'),
    ('TON', 'TON'),
    ('XMR', 'XMR'),
    ('DAI', 'DAI'),
    # ('TUSD', 'TUSD'),
]

PAYMENT_METHOD_CHOICES = [
    ('Tinkoff', 'Тинькофф'),
    ('Sber', 'Сбербанк'),
    ('Raiffeisenbank', 'Райффайзенбанк'),
    # ('MTS-Bank', 'МТС-Банк'),
    # ('QIWI', 'QIWI'),
    # ('Post-Bank', 'Почта Банк'),
    ('SBP', 'SBP'),
    ('BANK', 'BANK'),
    # ('Russia-Standart-Bank', 'Русский Стандарт'),
    # ('ЮMmoney', 'ЮMoney'),
]

EXCHANGES_CHOICES = [
    # ('binance', 'Binance'),
    # ('okx', 'Okx'),
    # ('bitget', 'Bitget'),
    ('exchange_bybit', 'Bybit'),
    ('exchange_huobi', 'Huobi'),
    ('exchange_garantex', 'Garantex'),
    ('exchange_bitpapa', 'Bitpapa'),
    ('exchange_beribit', 'Beribit'),
    ('exchange_hodlhodl', 'Hodl Hodl'),
    ('exchange_mexc', 'Mexc'),
    ('exchange_kucoin', 'Kucoin'),
    ('exchange_gateio', 'gateio'),
    ('exchange_totalcoin', 'Totalcoin'),
]


class CustomRadioSelect(forms.RadioSelect):
    def __init__(self, custom_param=None, *args, **kwargs):
        self.custom_param = custom_param
        super().__init__(*args, **kwargs)


    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        output = []
        options = self.choices
        for option_value, option_label in options:
            option_attrs = {'type': 'radio', 'name': name, 'value': option_value}
            if option_value == value:
                option_attrs['checked'] = 'checked'
            option_attrs['id'] = f"radio-{option_value}-{self.custom_param}"
            output.append(format_html(
                '<input {}> <label for="radio-{}-{}">{}</label>',
                flatatt(option_attrs), option_value, self.custom_param, option_label)
            )
        return mark_safe('\n'.join(output))


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        output = []
        options = self.choices
        for option_value, option_label in options:
            option_attrs = {'type': 'checkbox', 'name': name, 'value': option_value}
            if option_value in value:
                option_attrs['checked'] = 'checked'
            option_attrs['id'] = f"checkbox-{option_value}"
            output.append(format_html(
                '<input {}> <label for="checkbox-{}">{}</label>',
                flatatt(option_attrs), option_value, option_label)
            )
        return mark_safe('\n'.join(output))
    

class P2PFilters(forms.Form):
    crypto = forms.ModelChoiceField(
        initial={"name": "USDT"},
        widget=CustomRadioSelect(custom_param='crypto-filter'),
        queryset=CryptoFilterModel.objects.filter(active=True)
    )
    exchange = forms.ModelMultipleChoiceField(
        initial={"name": ["Bybit", "Huobi"]},
        widget=CustomCheckboxSelectMultiple,
        queryset=ExchangeFilterModel.objects.filter(active=True)
    )
    payments = forms.ModelMultipleChoiceField(
        initial={"name": ["Tinkoff", "Sber"]},
        widget=CustomCheckboxSelectMultiple,
        queryset=PaymentsFilterModel.objects.filter(active=True)
    )
    trade_type = forms.ModelChoiceField(
        initial={"name": "Taker - Maker"},
        widget=CustomRadioSelect(custom_param='trade-type-filter'),
        queryset=TradeTypeFilterModel.objects.filter(active=True)
    )
    lim_first = forms.IntegerField(initial=50000)
    lim_second = forms.IntegerField(initial=5000)
    ord_q = forms.IntegerField(
        initial=90, 
        widget=forms.NumberInput(attrs={
            'class': 'sidebar__select_item sidebar__select_spred hidden'
        })
    )
    ord_p = forms.IntegerField(        
        initial=90, 
        widget=forms.NumberInput(attrs={
            'class': 'sidebar__select_item sidebar__select_spred hidden'
        })
    )
    user_spread = forms.IntegerField(
        initial=10, 
        widget=forms.NumberInput(attrs={
            'class': 'sidebar__select_item sidebar__select_spred hidden'
        })
    )
    available_first = forms.IntegerField(required=False,)
    available_second = forms.IntegerField(required=False)
    only_stable_coin = forms.BooleanField(
        required=False, 
        initial=True,
        widget=forms.CheckboxInput(attrs={'value': 'boolenField'})
    )

class Filters(forms.Form):
    payment_methods = forms.MultipleChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=CustomCheckboxSelectMultiple(),
        initial=['Tinkoff', 'Sber'],
    )
    exchanges = forms.MultipleChoiceField(
        choices=EXCHANGES_CHOICES,
        widget=CustomCheckboxSelectMultiple(),
        initial=['exchange_bybit', 'exchange_totalcoin'],
    )
    crypto = forms.ChoiceField(
        choices = CRYPTO_CHOICES,
        widget = CustomRadioSelect(custom_param='p2p2'),
        initial = 'USDT',
    )
    crypto_multi = forms.ChoiceField(
        choices = CRYPTO_CHOICES_V2,
        widget = CustomRadioSelect(custom_param='p2p3'),
        initial = 'BTC',
    )
    trade_type = forms.ChoiceField(
        choices = TRADE_TYPE_CHOICES,
        widget = CustomRadioSelect(),
        initial = 'T-M_BUY-BUY',
    )
    lim_first = forms.IntegerField(initial=50000)
    lim_second = forms.IntegerField(initial=5000)
    ord_q = forms.IntegerField(
        initial=90,
        widget=forms.NumberInput(attrs={
            'class': 'sidebar__select_item sidebar__select_spred hidden'
        }),
    )
    ord_p = forms.IntegerField(
        initial=90,
        widget=forms.NumberInput(attrs={
            'class': 'sidebar__select_item sidebar__select_spred hidden'}),
    )
    user_spread = forms.IntegerField(
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'sidebar__select_item sidebar__select_spred hidden'}),
    )
    available_first = forms.IntegerField(
        required=False,
    )
    available_second = forms.IntegerField(
        required=False,
    )
    only_stable_coin = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'value': 'boolenField'}),
    )
