from base.views import BaseFormView


APP_NAME_URL = __package__ + '/'


class BlockSpreadTaleView(BaseFormView):
    url = APP_NAME_URL
    template_name = 'block_spreadtable.html'