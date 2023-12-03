from json import JSONDecodeError
import requests

from .forms import P2PFilters
from .serializers import P2PFilterSerializer
from base.views import BaseFormView, BaseAPIView

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


APP_NAME_URL = __package__ + '/'


class SpreadTableView(BaseFormView):
    template_name = 'spreadtable.html'
    url = APP_NAME_URL

    def get(self, request):
        context = self.get_context_data()
        context['filters'] = P2PFilters()
        return render(request, self.url + self.template_name, context)
    

class P2PLinks3View(APIView):
    def post(self, request):
        serializer = P2PFilterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        url = 'http://188.120.227.131:8001/api/v1/triangular-arbitrage/'
        response = requests.post(url, json=serializer.validated_data)
        return Response({'data': response.json()})
    

class P2PLinks2View(BaseAPIView):
    def post(self, request):
        serializer = P2PFilterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # url = 'http://188.120.227.131:8001/api/v1/binary-arbitrage/'
        url = 'http://172.27.0.5:8000/api/v1/binary-arbitrage/'
        # response = requests.post(url, json=serializer.validated_data)
        return Response(serializer.validated_data)
