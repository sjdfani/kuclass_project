from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from datetime import datetime, timedelta
from kuclass_project.settings import env
from .models import Job, JobState
from .tasks import send_email_deadline_job


def remind_deadline_jobs():
    jobs = Job.objects.filter(
        state=JobState.PENDING,
        end_at__lte=datetime.now(
            tz=pytz.utc)-timedelta(days=env('DEADLINE_JOBS_DAYS', cast=int)),
    )
    for job in jobs:
        send_email_deadline_job.delay(job.title, job.end_at, job.user.email)


def change_state_failed_jobs():
    Job.objects.filter(
        state=JobState.PENDING,
        end_at__lte=datetime.now(
            tz=pytz.utc)-timedelta(seconds=env('DELAY_CHANGE_STATE_JOBS_SECOND', cast=int)),
    ).update(state=JobState.FAILED)


def main():
    scheduler = BackgroundScheduler(timezone='MST')
    scheduler.add_job(remind_deadline_jobs, 'interval', minutes=2)
    scheduler.add_job(change_state_failed_jobs, 'interval', seconds=30)
    scheduler.start()
