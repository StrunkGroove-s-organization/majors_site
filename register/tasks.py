from accounts.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from myproject.celery import app

@app.task
def send_password_reset_email(email):

    user = User.objects.get(email=email)
    token = default_token_generator.make_token(user)

    subject = 'Восстановление пароля почты'
    sender = 'info@arbitools.ru'
    recipient = email
    valid_time = 24
    current_site = "arbitools.ru"
    protocol = 'https'

    msg_html = render_to_string('registration/password_reset_email.html', {
        'username': user.username,
        'protocol': protocol,
        'domain': current_site,
        'uid': urlsafe_base64_encode(str(user.pk).encode()),
        'token': token,
        'valid_time': valid_time,
    })

    message_error = f'Ваша сссылка для восстановления пароля:'
    send_mail(subject, message_error, sender, [recipient], html_message=msg_html, fail_silently=False)
    return None
