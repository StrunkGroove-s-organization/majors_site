from django import forms
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

from .models import (
    CryptoFilterModel, ExchangeFilterModel, PaymentsFilterModel,
    TradeTypeFilterModel,
)


class CustomRadioSelect(forms.RadioSelect):
    def __init__(self, custom_param=None, custom_initial=1, *args, **kwargs):
        self.custom_param = custom_param
        self.custom_initial = custom_initial
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        output = []
        options = self.choices
        for option_value, option_label in options:
            option_attrs = {'type': 'radio', 'name': name, 'value': option_value}
            if option_value == self.custom_initial:
                option_attrs['checked'] = 'checked'
            option_attrs['id'] = f"radio-{self.custom_param}-{option_value}-{value}"
            output.append(format_html(
                '<input {}> <label for="radio-{}-{}-{}">{}</label>',
                flatatt(option_attrs), self.custom_param, option_value, value, option_label)
            )
        return mark_safe('\n'.join(output))


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, custom_param=None, custom_initial=[1, 2], *args, **kwargs):
        self.custom_param = custom_param
        self.custom_initial = custom_initial
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        output = []
        options = self.choices
        for option_value, option_label in options:
            option_attrs = {'type': 'checkbox', 'name': name, 'value': option_value}
            if option_value in self.custom_initial:
                option_attrs['checked'] = 'checked'
            option_attrs['id'] = f"checkbox-{self.custom_param}-{option_value}"
            output.append(format_html(
                '<input {}> <label for="checkbox-{}-{}">{}</label>',
                flatatt(option_attrs), self.custom_param, option_value, option_label)
            )
        return mark_safe('\n'.join(output))
    

class P2PFilters(forms.Form):
    try:
        crypto_initial = CryptoFilterModel.objects.filter(default=True).first().id
        crypto_queryset = CryptoFilterModel.objects.filter(active=True)
    except Exception as e:
        crypto_initial = 1 
        crypto_queryset = None

    crypto = forms.ModelChoiceField(
        widget=CustomRadioSelect(
            custom_param='crypto-filter',
            custom_initial=crypto_initial
        ),
        queryset=crypto_queryset
    )

    try:
        exchanges_initial = list(ExchangeFilterModel.objects \
                                .filter(default=True) \
                                .values_list('id', flat=True))
        exchanges_queryset = ExchangeFilterModel.objects.filter(active=True)
    except Exception as e:
        exchanges_initial = [1, 2]
        exchanges_queryset = None

    exchanges = forms.ModelMultipleChoiceField(
        initial={"name": ["Bybit", "Huobi"]},
        widget=CustomCheckboxSelectMultiple(
            custom_param='exchange-filter', 
            custom_initial=exchanges_initial
        ),
        queryset=exchanges_queryset
    )

    try:
        payment_methods_initial = list(PaymentsFilterModel.objects \
                                    .filter(default=True) \
                                    .values_list('id', flat=True))
        payment_methods_queryset = PaymentsFilterModel.objects.filter(active=True)
    except Exception as e:
        payment_methods_initial = [1, 2] 
        payment_methods_queryset = None

    payment_methods = forms.ModelMultipleChoiceField(
        widget=CustomCheckboxSelectMultiple(
            custom_param='payments-filter', 
            custom_initial=payment_methods_initial
        ),
        queryset=payment_methods_queryset
    )

    try:
        trade_type_initial = TradeTypeFilterModel.objects.filter(default=True).first().id
        trade_type_queryset = TradeTypeFilterModel.objects.filter(active=True)
    except Exception as e:
        trade_type_initial = 1 
        trade_type_queryset = None

    trade_type = forms.ModelChoiceField(widget=CustomRadioSelect(
                                            custom_param='trade-type-filter', 
                                            custom_initial=trade_type_initial
                                        ), 
                                        queryset=trade_type_queryset)
    
    lim_first = forms.IntegerField(initial=50000, required=False)
    lim_second = forms.IntegerField(initial=5000, required=False)
    ord_q = forms.IntegerField(required=False,
                               initial=90, 
                               widget=forms.NumberInput(attrs={
                                   'class': 'sidebar__select_item sidebar__select_spred hidden'}))
    
    ord_p = forms.IntegerField(required=False, 
                               initial=90, 
                               widget=forms.NumberInput(attrs={
                                   'class': 'sidebar__select_item sidebar__select_spred hidden'}))
    
    user_spread = forms.IntegerField(required=False,
                                     initial=10, 
                                     widget=forms.NumberInput(attrs={
                                         'class': 'sidebar__select_item sidebar__select_spred hidden'}))
    
    available_first = forms.IntegerField(required=False)
    available_second = forms.IntegerField(required=False)
    only_stable_coin = forms.BooleanField(required=False, 
                                          initial=True,
                                          widget=forms.CheckboxInput(attrs={
                                              'value': 'boolenField'}))
