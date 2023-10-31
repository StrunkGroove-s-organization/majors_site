from base.views import BaseFormView


APP_NAME_URL = __package__ + '/'


class IndexView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'index.html'

class EmptyView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'empty.html'

class Cookies(BaseFormView):
    url = APP_NAME_URL
    template_name = 'cookies.html'