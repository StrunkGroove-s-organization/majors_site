from rest_framework.response import Response
from rest_framework.views import APIView


class PaymentPlisio(APIView):
    def get(self, request):
        return Response({'title': 'Angelina Jolie'})
    
    def post(self, request):
        return Response({'title': 'Jennifer Shrader Lawrence'})