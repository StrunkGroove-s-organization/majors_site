from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from refferal.models import Referral
from accounts.models import User


class Order(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='user_order'
    )
    type = models.CharField(max_length=50)
    days = models.IntegerField()
    currency = models.CharField(max_length=50)
    token = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=40, decimal_places=2, default=0.0)
    referral = models.ForeignKey(
        Referral,
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='order_referral'
    )

    def __str__(self):
        return f"Order {self.id} - {self.type}"


class CompleteOrder(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='order'
    )

    def __str__(self):
        return f"CompleteOrder {self.id}"


@receiver(post_save, sender=CompleteOrder)
def update_referral(sender, instance, created, **kwargs):
    if created:
        referral = instance.order.referral
        if referral:
            referral.earnings += (instance.order.amount - 1) * ((referral.refferal_percent) / 100)
            referral.save()
