from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_confirmation_email(email: str, code: str) -> None:
    send_mail(
        subject='Подтверждение регистрации',
        message=f'Ваш код подтверждения: {code}\nКод действует 5 минут.',
        from_email=None,  # берётся из DEFAULT_FROM_EMAIL
        recipient_list=[email],
    )
