from django.contrib import admin
from .models import Order, CompleteOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = ('email', 'type', 'days', 'timestamp', 'amount', 'token')
    search_fields = ('token', 'email')


class CompleteOrderAdmin(admin.ModelAdmin):
    list_display = ('email', 'type', 'days', 'timestamp', 'currency', 'amount_crypto', 'token')
    search_fields = ('token', 'email')

admin.site.register(Order, OrderAdmin)
admin.site.register(CompleteOrder, CompleteOrderAdmin)
