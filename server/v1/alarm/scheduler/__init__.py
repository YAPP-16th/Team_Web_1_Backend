from datetime import datetime

from server.models.alarm import Alarm
from server.v1.alarm.channels import send_message


def get_alarms():
    now = datetime.now()
    for qs in Alarm.objects.filter(reserved_time__year=now.year,
                                   reserved_time__month=now.month,
                                   reserved_time__day=now.day,
                                   reserved_time__hour=now.hour,
                                   reserved_time__minute=now.minute):
        # 여기서 소켓으로 메세지 전송한다.
        send_message(qs)
