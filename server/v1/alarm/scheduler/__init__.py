from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import register_events, register_job

from server.models.alarm import Alarm
from server.v1.alarm.consumer import announce

SCHEDULER = BackgroundScheduler(settings.SCHEDULER_CONFIG)


@register_job(SCHEDULER, "cron", minute="*/1", second="0", id=f"job")
def get_alarms():
    now = datetime.now()
    for qs in Alarm.objects.filter(reserved_time__year=now.year,
                                   reserved_time__month=now.month,
                                   reserved_time__day=now.day,
                                   reserved_time__hour=now.hour,
                                   reserved_time__minute=now.minute):
        # 여기서 소켓으로 메세지 전송한다.
        announce(qs)


def start():
    register_events(SCHEDULER)
    SCHEDULER.start()
