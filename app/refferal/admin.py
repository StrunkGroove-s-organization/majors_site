from django.contrib import admin
from .models import Referral


class ReferralAdmin(admin.ModelAdmin):
    list_display = ('refferal_percent', 'referral_code', 'created_at', 
                    'clicks', 'earnings', 'complete_earnings'
                    )

admin.site.register(Referral, ReferralAdmin)

