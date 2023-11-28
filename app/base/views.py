from datetime import datetime, timezone

from django.shortcuts import render
from django.views import View

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from accounts.forms import CustomUserRegistrationForm, LoginForm


class BaseFormView(View):    
    def get_context_data(self):
        return {
            'login_form': LoginForm(),
            'register_form': CustomUserRegistrationForm(),
        }

    def get(self, request):
        return render(
            request, self.url + self.template_name, self.get_context_data()
        )


class HasSubscriptionPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        status = request.user.is_staff
        if status: return True

        status = request.user.has_infinity_subscription
        if status: return True

        if request.user.subscription_end >= datetime.now(timezone.utc): return True

        return False


class BaseAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasSubscriptionPermission]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        response_data = self.process_request(request, serializer.validated_data)
        return Response(response_data)
        