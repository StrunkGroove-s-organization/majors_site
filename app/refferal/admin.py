from django.contrib import admin
from .models import Referral


class ReferralAdmin(admin.ModelAdmin):
    list_display = ('user', 'refferal_percent', 'referral_code', 'created_at', 
                    'clicks', 'invited_users', 
                    'payments', 'complete_payments', 'earnings', 'complete_earnings'
                    )

admin.site.register(Referral, ReferralAdmin)

