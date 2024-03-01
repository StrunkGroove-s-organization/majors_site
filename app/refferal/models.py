import random
import string

import requests

from django.db import models
# from payment.models import Order, CompleteOrder
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.cache import cache


KEY_BNB = 'key_bnb_binance'


class Referral(models.Model):
    refferal_percent = models.DecimalField(max_digits=5, decimal_places=2, default=30)
    referral_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)
    earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    complete_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    must_be_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    @staticmethod
    def _generate_referral_code() -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

    @staticmethod
    def _get_binance_price(symbol='BNBUSDT') -> float:
        api_url = "https://api.binance.com/api/v3/ticker/price"
        response = requests.get(api_url, params={"symbol": symbol})
        response.raise_for_status()
        data = response.json()
        spot_price = float(data["price"])
        cache.set(KEY_BNB, spot_price, 60 * 15)
        return spot_price
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self._generate_referral_code()
        self.must_be_paid = self.earnings - self.complete_earnings
        super().save(*args, **kwargs)

    def increment_clicks(self):
        self.clicks += 1
    
    def calculate_earnings(self) -> float:
        bnbusdt_price = cache.get(KEY_BNB)
        if not bnbusdt_price:
            bnbusdt_price = self._get_binance_price()

        total_earnings = 0

        for order in self.complete_payments.all():
            if order.currency in ['USDT_TRX', 'USDT_BSC']:
                total_earnings += order.amount_crypto
            elif order.currency in ['BNB']:
                total_earnings += order.amount_crypto * bnbusdt_price
        
        total_earnings = float(total_earnings) - self.complete_earnings
        return total_earnings

    # def __str__(self):
    #     return f"Referral for {self.user.username}"
