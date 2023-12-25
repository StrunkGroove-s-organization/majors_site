from django.db import models
from accounts.models import User
from payment.models import Order, CompleteOrder


class Referral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    def increment_clicks(self):
        self.clicks += 1
        self.save()

    def __str__(self):
        return f"Referral for {self.user.username}"
    