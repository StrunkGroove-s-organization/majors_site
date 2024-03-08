from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

from .models import UserPageVisitModel


class UserPageVisitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path

        if self._is_html_path(path):
            user = request.user
            UserPageVisitModel.objects.create(
                user=user if user.is_authenticated else None,
                page_url=path
            )

    @staticmethod
    def _is_html_path(path):
        if '.' in path:
            return False
        return True




