from django.views import View
from django.shortcuts import render

from accounts.forms import CustomUserRegistrationForm, LoginForm


APP_NAME = __package__


class BaseFormView(View):
    def get(self, request):
        return render(
            request, self.template_path, {
            'login_form': LoginForm(),
            'register_form': CustomUserRegistrationForm(),
        })
    

class IndexView(BaseFormView):
    template_name = "index.html"
    template_path = APP_NAME + "/" + template_name


class EmptyView(BaseFormView):
    template_name = "empty.html"
    template_path = APP_NAME + "/" + template_name


class Cookies(BaseFormView):
    template_name = "cookies.html"
    template_path = APP_NAME + "/" + template_name


class PrivacyPolicy(BaseFormView):
    template_name = "privacy_policy.html"
    template_path = APP_NAME + "/" + template_name


class TermsOfUse(BaseFormView):
    template_name = "terms_of_use.html"
    template_path = APP_NAME + "/" + template_name


class DenialOfResponsibility(BaseFormView):
    template_name = "denial_of_responsibility.html"
    template_path = APP_NAME + "/" + template_name
    

class CalculatorSpread(BaseFormView):
    template_name = "calculator_spread.html"
    template_path = APP_NAME + "/" + template_name