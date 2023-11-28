from accounts.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from myproject.celery import app
from django.utils.html import strip_tags


@app.task
def send_gratitude_for_payment(email):

    user = User.objects.get(email=email)
    subject = 'Команда ArbiTools'
    sender = 'info@arbitools.ru'
    recipient = email
    current_site = "arbitools.ru"
    
    context = {
        'user': user,
        'current_site': current_site,
    }

    html_message = render_to_string('payment/gratitude_email.html', context)
    
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        sender,
        [recipient],
        html_message=html_message,
        fail_silently=False,
    )

