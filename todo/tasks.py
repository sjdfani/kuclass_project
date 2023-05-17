from celery import shared_task
from django.core.mail import send_mail
from kuclass_project.settings import env
from datetime import datetime


@shared_task
def send_email_deadline_job(job_title: str, job_end_time: float, to_: str):
    subject = 'Job deadline'
    deadline = datetime.fromtimestamp(job_end_time)
    message = f'''
        <<< Job deadline >>>
        Your Job with below information will fail if you don't anything.
        Job title: {job_title}
        Job deadline: {deadline}
        Do it before end deadline.
        Good luck.
    '''
    send_mail(
        subject, message, env('EMAIL_USER'), [to_]
    )
