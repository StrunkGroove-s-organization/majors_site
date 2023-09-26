from accounts.forms import CustomUserRegistrationForm, LoginForm

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render
from django.views import View


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


class BaseAPIView(APIView):
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            response_data = self.process_request(serializer.validated_data)
            return Response(response_data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)