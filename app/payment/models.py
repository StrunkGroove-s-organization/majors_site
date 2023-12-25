from django.db import models


class Order(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50)
    days = models.IntegerField()
    token = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=40, decimal_places=15, default=0.0)

    def __str__(self):
        return f"Order {self.id} - {self.email}"


class CompleteOrder(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50)
    days = models.IntegerField()
    token = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    amount_crypto = models.DecimalField(max_digits=40, decimal_places=15, default=0.0)

    def __str__(self):
        return f"CompleteOrder {self.id} - {self.email}"


