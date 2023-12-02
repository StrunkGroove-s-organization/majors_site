from django.contrib import admin
from .models import (
    CryptoFilterModel, ExchangeFilterModel, PaymentsFilterModel, 
    TradeTypeFilterModel
)


class BaseFilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active',)
    search_fields = ('name',)

admin.site.register(CryptoFilterModel, BaseFilterAdmin)
admin.site.register(ExchangeFilterModel, BaseFilterAdmin)
admin.site.register(PaymentsFilterModel, BaseFilterAdmin)
admin.site.register(TradeTypeFilterModel, BaseFilterAdmin)
