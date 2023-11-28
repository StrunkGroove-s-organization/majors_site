from django import forms
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe


class CustomRadioSelectV2(forms.RadioSelect):
    def __init__(self, custom_param=None, *args, **kwargs):
        self.custom_param = custom_param
        super().__init__(*args, **kwargs)


    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        output = []
        options = self.choices.copy()
        for option_value, option_label in options:
            option_attrs = {'type': 'radio', 'name': name, 'value': option_value}
            option_value = option_value.split('_')[1]
            if option_value == value:
                option_attrs['checked'] = 'checked'
            option_attrs['id'] = f"radio-{option_value}-{self.custom_param}"
            option_attrs['class'] = "premium__rate-item"
            output.append(format_html(
                '<div class="premium__period-item"><input {}> <label for="radio-{}-{}">{}</label></div>',
                flatatt(option_attrs), option_value, self.custom_param, option_label)
            )
        return mark_safe('\n'.join(output))


class CustomRadioSelect(forms.RadioSelect):
    def __init__(self, custom_param=None, *args, **kwargs):
        self.custom_param = custom_param
        super().__init__(*args, **kwargs)


    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        output = []
        options = self.choices.copy()
        for option_value, option_label in options:
            option_attrs = {'type': 'radio', 'name': name, 'value': option_value}
            if option_value == value:
                option_attrs['checked'] = 'checked'
            option_attrs['id'] = f"radio-{option_value}-{self.custom_param}"
            option_attrs['class'] = "premium__rate-item"
            output.append(format_html(
                '<div class="premium__period-item"><input {}> <label for="radio-{}-{}">{}</label></div>',
                flatatt(option_attrs), option_value, self.custom_param, option_label)
            )
        return mark_safe('\n'.join(output))


class Subscription(forms.Form):
    POSITION_CHOICES = [
        ('2_test_10', 'Пробный'),
        ('30_profi_28', 'Стандарт'),
        ('1000_infinity_500', 'Вечный'),
    ]
    CURRENCY = [
        ('USDT_TRX', 'USDT TRC-20'),
        ('USDT_BSC', 'USDT BEP-20'),
        ('BNB', 'BNB BEP-20'),
    ]
    subscription = forms.ChoiceField(
        choices = POSITION_CHOICES,
        widget = CustomRadioSelectV2(custom_param='subscription'),
        initial='profi',
    )
    currency = forms.ChoiceField(
        choices = CURRENCY,
        widget = CustomRadioSelect(custom_param='currency'),
        initial='BNB',
    )
