from django.contrib import admin
from .models import User
 
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 
                    'has_infinity_subscription', 'subscription_start', 
                    'subscription_end', 'type_subscription', 
                    'referral_info', 'referral_belongs_to'
                    )
    search_fields = ('username', 'email')

admin.site.register(User, CustomUserAdmin)
