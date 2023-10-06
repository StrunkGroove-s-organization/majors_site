from .forms import Filters
from .services import p2plinks_3, p2plinks_2
from .serializers import P2PLinksSerializer
from base.views import BaseFormView, BaseAPIView

from django.shortcuts import render


APP_NAME_URL = __package__ + '/'


class SpreadTableView(BaseFormView):
    template_name = 'spreadtable.html'
    url = APP_NAME_URL

    def get(self, request):
        filters = Filters()
        context = self.get_context_data()
        context['filters'] = filters
        return render(request, self.url + self.template_name, context)
    

class P2PLinks3View(BaseAPIView):
    def get_serializer(self, data):
        return P2PLinksSerializer(data=data)

    def process_request(self, request, validated_data):
        exchange_ads = p2plinks_3(validated_data)
        return {'data': exchange_ads}


class P2PLinks2View(BaseAPIView):
    def get_serializer(self, data):
        return P2PLinksSerializer(data=data)

    def process_request(self, request, validated_data):
        exchange_ads = p2plinks_2(validated_data)
        return {'data': exchange_ads}
