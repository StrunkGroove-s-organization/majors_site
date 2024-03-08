from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.utils import timezone

from .models import UserPageVisitModel
from accounts.models import User


APP_NAME = __package__


def is_superuser(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Доступ запрещен. Требуется статус суперпользователя.")
    return wrapped_view


class AdminPanelView(View):
    template_name = "admin_panel.html"
    template_path = APP_NAME + "/" + template_name

    @method_decorator(login_required)
    @method_decorator(is_superuser)
    def get(self, request):
        return render(request, self.template_path)


class AnalysisView(View):
    template_name = "analysis.html"
    template_path = APP_NAME + "/" + template_name

    @method_decorator(login_required)
    @method_decorator(is_superuser)
    def get(self, request):
        records = UserPageVisitModel.objects.all()

        current_datetime = timezone.now()
        users_last_day, unique_users_last_day = self._count_analysis(
            current_datetime=current_datetime, days=1, records=records
        )
        users_last_week, unique_users_last_week = self._count_analysis(
            current_datetime=current_datetime, days=7, records=records
        )
        users_last_month, unique_users_last_month = self._count_analysis(
            current_datetime=current_datetime, days=30, records=records
        )

        anonymous_last_day, anonymous_users_last_day = self._count_analysis(
            current_datetime=current_datetime, days=1, records=records, anonymous=True
        )
        anonymous_last_week, anonymous_users_last_week = self._count_analysis(
            current_datetime=current_datetime, days=7, records=records, anonymous=True
        )
        anonymous_last_month, anonymous_users_last_month = self._count_analysis(
            current_datetime=current_datetime, days=30, records=records, anonymous=True
        )

        users_records = User.objects.all()

        users_with_active_subscription = users_records.filter(subscription_end__gt=datetime.now()).count()
        users_with_infinity_subscription = users_records.filter(has_infinity_subscription=True).count()

        users_registered_last_day = self._users_registrations(
            current_datetime=current_datetime, days=1, records=users_records
        )
        users_registered_last_week = self._users_registrations(
            current_datetime=current_datetime, days=7, records=users_records
        )
        users_registered_last_month = self._users_registrations(
            current_datetime=current_datetime, days=30, records=users_records
        )

        analysis = {
            "users_last_day": users_last_day,
            "unique_users_last_day": unique_users_last_day,
            "users_last_week": users_last_week,
            "unique_users_last_week": unique_users_last_week,
            "users_last_month": users_last_month,
            "unique_users_last_month": unique_users_last_month,

            "anonymous_last_day": anonymous_last_day,
            "anonymous_last_week": anonymous_last_week,
            "anonymous_last_month": anonymous_last_month,

            "users_with_active_subscription": users_with_active_subscription,
            "users_with_infinity_subscription": users_with_infinity_subscription,

            "users_registered_last_day": users_registered_last_day,
            "users_registered_last_week": users_registered_last_week,
            "users_registered_last_month": users_registered_last_month,
        }
        return render(request, self.template_path, {"analysis": analysis, "records": records})

    @staticmethod
    def _users_registrations(current_datetime, days, records) -> int:
        time_passed = current_datetime - timezone.timedelta(days=days)
        return records.filter(registration_date__gte=time_passed).count()
    
    @staticmethod
    def _count_analysis(current_datetime, days, records: list[UserPageVisitModel], anonymous=False) -> tuple[int, int]:
        time_passed = current_datetime - timezone.timedelta(days=days)
        users = records.filter(visit_time__gte=time_passed, user__isnull=anonymous).count()
        if anonymous is True:
            return users, False

        unique_users = records.filter(visit_time__gte=time_passed, user__isnull=anonymous).values('user').distinct().count()
        return users, unique_users