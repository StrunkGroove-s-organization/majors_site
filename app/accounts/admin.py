from django.contrib import admin
rom django.contrib.auth.admin import UserAdmin
from .models import User
 
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 
                    'has_infinity_subscription', 'subscription_start', 
                    'subscription_end', 'type_subscription'
                    )
    search_fields = ('username', 'email')

admin.site.register(User, CustomUserAdmin)
