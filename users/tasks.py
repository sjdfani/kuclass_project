from celery import shared_task
from django.core.mail import send_mail
from kuclass_project.settings import env


@shared_task
def send_email_forgot_password(code: str, to_: str):
    subject = 'Forgot password'
    message = f'''
        <<< Forgot Password >>>
        Please Enter bellow code in input.
        code: {code}
        If you don't request to change password just ignore this email.
        Good luck. 
    '''
    send_mail(
        subject, message, env('EMAIL_USER'), [to_]
    )
