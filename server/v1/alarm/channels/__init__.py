from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

from urlink.settings import REDIS

CHANNEL_LAYER = get_channel_layer()


@database_sync_to_async
def update_alarm_transmission_status(alarm):
    alarm.has_been_sent = True
    alarm.save()


def send_message(alarm, debug=False):
    channel_layer = get_channel_layer() if debug else CHANNEL_LAYER

    user_id = str(alarm.user.id)
    user_group_list = REDIS.lrange(user_id, 0, -1)

    if user_group_list:
        message = {
            'id': alarm.id,
            'name': alarm.name,
            'reserved_time': str(alarm.reserved_time),
            'url_path': alarm.url.path,
            'url_title': alarm.url.title,
            'url_description': alarm.url.description,
            'url_image_path': alarm.url.image_path,
            'url_favicon_path': alarm.url.favicon_path,
            'alarm_has_read': alarm.has_read,
            'alarm_has_done': alarm.has_done,
        }
        for user_group in user_group_list:
            group = user_group.decode('utf-8')
            async_to_sync(channel_layer.group_send)(
                group=group,
                message={
                    'type': 'send_message',
                    'message': message,
                    'status': 'alarm'
                }
            )
    async_to_sync(update_alarm_transmission_status)(alarm)
