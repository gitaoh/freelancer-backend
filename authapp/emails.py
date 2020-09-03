from django.core.mail import send_mail


def send_email_to_user(subject, message, from_email):
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[],
        from_email=from_email,
        # if false will raise an smtplib.SMTPException
        fail_silently=True,
        html_message=message,
        connection=''
    )
