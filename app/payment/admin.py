from django.contrib import admin
from .models import Order, CompleteOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'days', 'timestamp', 'amount', 'token')
    search_fields = ('token', 'user')


class CompleteOrderAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'order')
    search_fields = ('order',)


admin.site.register(Order, OrderAdmin)
admin.site.register(CompleteOrder, CompleteOrderAdmin)
