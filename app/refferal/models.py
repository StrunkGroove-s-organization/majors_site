import requests

from django.db import models
from accounts.models import User
from payment.models import Order, CompleteOrder
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.cache import cache


KEY_BNB = 'key_bnb_binance'


class Referral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    refferal_percent = models.FloatField(default=30)
    referral_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)
    invited_users = models.ManyToManyField(User,
                                           blank=True, 
                                           related_name="invited_users"
                                           )
    payments = models.ManyToManyField(Order,
                                      blank=True, 
                                      related_name="payments"
                                      )
    complete_payments = models.ManyToManyField(CompleteOrder, 
                                               blank=True, 
                                               related_name="complete_payments"
                                               )
    earnings = models.FloatField(default=0)
    complete_earnings = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.earnings = self.earnings - self.complete_earnings
        super().save(*args, **kwargs)

    def increment_clicks(self):
        self.clicks += 1
        self.save()

    def __get_binance_price(self, symbol='BNBUSDT') -> float:
        api_url = "https://api.binance.com/api/v3/ticker/price"
        response = requests.get(api_url, params={"symbol": symbol})
        response.raise_for_status()
        data = response.json()
        spot_price = float(data["price"])
        cache.set(KEY_BNB, spot_price, 60 * 15)
        return spot_price
    
    def calculate_earnings(self) -> float:
        bnbusdt_price = cache.get(KEY_BNB)
        if not bnbusdt_price:
            bnbusdt_price = self.__get_binance_price()

        total_earnings = 0

        for order in self.complete_payments.all():
            if order.currency in ['USDT_TRX', 'USDT_BSC']:
                total_earnings += order.amount_crypto
            elif order.currency in ['BNB']:
                total_earnings += order.amount_crypto * bnbusdt_price
        
        total_earnings = float(total_earnings) - self.complete_earnings
        return total_earnings

    def __str__(self):
        return f"Referral for {self.user.username}"

@receiver(m2m_changed, sender=Referral.complete_payments.through)
def update_earnings(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        instance.earnings = instance.calculate_earnings()
        instance.save()