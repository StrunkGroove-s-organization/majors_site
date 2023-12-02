from django.db import models


class AbstractFilterModel(models.Model):
    name = models.CharField(max_length=10, unique=True)
    active = models.BooleanField(default=False)
  
    class Meta: 
        abstract = True

    def __str__(self):
        return self.name


class CryptoFilterModel(AbstractFilterModel):
    pass
    

class ExchangeFilterModel(AbstractFilterModel):
    pass


class PaymentsFilterModel(AbstractFilterModel):
    pass
    

class TradeTypeFilterModel(AbstractFilterModel):
    CHOICES = [
        ('Maker - Maker', 'M-M_SELL-BUY' ),
        ('Maker - Taker', 'M-T_SELL-SELL'),
        ('Taker - Maker', 'T-M_BUY-BUY'),
        ('Taker - Taker', 'T-T_BUY-SELL'),
    ]

    name = models.CharField(max_length=20, unique=True, choices=CHOICES)