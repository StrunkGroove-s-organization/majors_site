from django.db import models
from accounts.models import User


class FavouriteThreeModel(models.Model):
    base_crypto = models.CharField(max_length=10)
    exchange = models.CharField(max_length=50)
    best_change_exchange = models.IntegerField()
    id_best_change_give = models.IntegerField()
    id_best_change_get = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class FavouriteTwoModel(models.Model):
    first_exchange = models.CharField(max_length=50)
    second_exchange = models.CharField(max_length=50)
    first_give = models.CharField(max_length=50)
    first_get = models.CharField(max_length=50)
    second_give = models.CharField(max_length=50)
    second_get = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class AllLinksHash(models.Model):
    hash_info = models.CharField(max_length=150)
    hash_info_ex = models.CharField(max_length=150)
    base_token = models.CharField(max_length=50)
    id_first_token = models.CharField(max_length=50)
    id_second_token = models.CharField(max_length=50)
    id_best_change_exchange = models.CharField(max_length=50)
    