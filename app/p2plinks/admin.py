from django.contrib import admin
from .models import (
    CryptoFilterModel, ExchangeFilterModel, PaymentsFilterModel, 
    TradeTypeFilterModel
)


class BaseFilterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active', 'default')
    list_filter = ('active', 'default')
    search_fields = ('name',)

admin.site.register(CryptoFilterModel, BaseFilterAdmin)
admin.site.register(ExchangeFilterModel, BaseFilterAdmin)
admin.site.register(PaymentsFilterModel, BaseFilterAdmin)
admin.site.register(TradeTypeFilterModel, BaseFilterAdmin)
