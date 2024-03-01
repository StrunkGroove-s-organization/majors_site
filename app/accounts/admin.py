from django.contrib import admin
from .models import User
 

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 
                    'has_infinity_subscription', 'subscription_start', 
                    'subscription_end', 'type_subscription', 
                    'referral_info', 'referral_belongs_to'
                    )
    search_fields = ('username', 'email')

    actions = ['restore_referral_systems']

    def restore_referral_systems(self, request, queryset) -> None:
        for record in queryset:
            if not record.referral_info:
                record.restore_referral_systems()
    
    restore_referral_systems.short_description = "Создать запись в реферальной модели"

admin.site.register(User, CustomUserAdmin)