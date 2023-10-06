from base.views import BaseFormView


APP_NAME_URL = __package__ + '/'


class СookiesView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'cookies.html'