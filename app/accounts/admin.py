from django.contrib import admin
from .models import User
 
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 
                    'has_infinity_subscription', 'subscription_start', 
                    'subscription_end', 'type_subscription'
                    )
    search_fields = ('username', 'email')

admin.site.register(User, CustomUserAdmin)
