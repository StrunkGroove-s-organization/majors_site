from django.http import JsonResponse
from accounts.models import User
from .tasks import send_password_reset_email

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            validate_email(email)
        except ValidationError:
            data = 'Недопустимый адрес электронной почты'
            return JsonResponse(data, status=400, safe=False)

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            data = 'Этот адрес электронной почты не существует'
            return JsonResponse(data, status=400, safe=False)

        send_password_reset_email.delay(email)

        data = 'Проверьте свою электронную почту для сброса пароля'
        return JsonResponse(data, status=200, safe=False)


