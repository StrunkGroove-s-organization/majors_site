from functools import wraps

from django.utils import timezone
from django.shortcuts import render
from django.utils.decorators import method_decorator

from accounts.forms import CustomUserRegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required

from .forms import Filters
from .services import p2plinks_3, p2plinks_2
from .serializers import P2PLinksSerializer
from base.views import BaseFormView, BaseAPIView


APP_NAME_URL = __package__ + '/'


def check_subscription(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.has_infinity_subscription and timezone.now() >= user.subscription_end:
            register_form = CustomUserRegistrationForm()
            login_form = LoginForm()
            filters = Filters()
            return render(request, 'p2plinks/spreadtable.html', {
                'filters': filters,
                'login_form': login_form,
                'register_form': register_form,
            })

        return view_func(request, *args, **kwargs)

    return _wrapped_view


class SpreadTableView(BaseFormView):
    template_name = 'spreadtable.html'
    url = APP_NAME_URL

    def get(self, request):
        filters = Filters()
        context = self.get_context_data()
        context['filters'] = filters
        return render(request, self.url + self.template_name, context)
    

# @method_decorator(login_required(login_url='spreadtable'))
# @method_decorator(check_subscription)
class P2PLinks3View(BaseAPIView):
    def get_serializer(self, data):
        return P2PLinksSerializer(data=data)

    def process_request(self, validated_data):
        exchange_ads = p2plinks_3(validated_data)
        return {'data': exchange_ads}

# class P2PLinks3View(APIView):

#     @method_decorator(login_required(login_url='spreadtable'))
#     @method_decorator(check_subscription)
#     def post(self, request):
#         serializer = P2PLinksSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         exchange_ads = p2plinks_3(serializer)
#         return {'data': exchange_ads}


# @method_decorator(login_required(login_url='spreadtable'))
# @method_decorator(check_subscription)
class P2PLinks2View(BaseAPIView):
    def get_serializer(self, data):
        return P2PLinksSerializer(data=data)

    def process_request(self, validated_data):
        exchange_ads = p2plinks_2(validated_data)
        return {'data': exchange_ads}


# class P2PLinks2View(APIView):

#     @method_decorator(login_required(login_url='spreadtable'))
#     @method_decorator(check_subscription)
#     def post(self, request):
#         serializer = P2PLinksSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(
#                 serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST, 
#             )

#         exchange_ads = p2plinks_2(serializer)
#         return Response(
#             {'data': exchange_ads},
#             status=status.HTTP_200_OK
#         )