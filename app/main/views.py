from django.views import View
from django.shortcuts import render

from base.views import BaseFormView
from accounts.forms import CustomUserRegistrationForm, LoginForm
from p2plinks.forms import P2PFilters


APP_NAME_URL = __package__ + '/'
APP_NAME = __package__


class IndexView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'index.html'

class EmptyView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'empty.html'

class Cookies(BaseFormView):
    url = APP_NAME_URL
    template_name = 'cookies.html'

class CalculatorSpread(BaseFormView):
    url = APP_NAME_URL
    template_name = 'calculator_spread.html'


class TestView(View):
    def get(self, request):
        return render(
                request, APP_NAME + '/' + 'test.html', {
                'login_form': LoginForm(),
                'register_form': CustomUserRegistrationForm(),
                'filters': P2PFilters(),
            }
        )