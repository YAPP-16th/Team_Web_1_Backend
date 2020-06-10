import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from server.models.alarm import Alarm

CHANNEL_LAYER = get_channel_layer()


@database_sync_to_async
def update_alarm_transmission_status(alarm):
    alarm.has_been_sent = True
    alarm.save()


def send_message(alarm, debug=False):
    channel_layer = get_channel_layer() if debug else CHANNEL_LAYER

    group = str(alarm.user.id)
    async_to_sync(channel_layer.group_send)(
        group=group,
        message={
            'type': 'send_message',
            'message': {
                'id': alarm.id,
                'name': alarm.name,
                'reserved_time': str(alarm.reserved_time),
                'url_path': alarm.url.path,
                'url_title': alarm.url.title,
                'url_description': alarm.url.description,
                'url_image_path': alarm.url.image_path,
                'url_favicon_path': alarm.url.favicon_path
            }
        }
    )
    async_to_sync(update_alarm_transmission_status)(alarm)


class AlarmConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 같은 정보를 받는 분리된 사용자로 취급해야하는데..
        await self.channel_layer.group_add(
            group=str(self.scope['user'].id),
            channel=self.channel_name
        )

        await self.accept()
        await self.send_past_alarms()

    async def send_past_alarms(self):
        past_alarms = await self.get_past_alarms(self.scope['user'])
        await self.channel_layer.group_send(
            group=str(self.scope['user'].id),
            message={
                'type': 'send_message',
                'message': past_alarms
            }
        )

    @database_sync_to_async
    def get_past_alarms(self, user):
        results = []
        alarms = Alarm.objects.filter(user=user, has_been_sent=True, has_done=False)
        for alarm in alarms:
            results.append({
                'id': alarm.id,
                'name': alarm.name,
                'reserved_time': str(alarm.reserved_time),
                'url_path': alarm.url.path,
                'url_title': alarm.url.title,
                'url_description': alarm.url.description,
                'url_image_path': alarm.url.image_path,
                'url_favicon_path': alarm.url.favicon_path
            })
        return results

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            group=str(self.scope['user'].id),
            channel=self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        alarm_id = message.get('alarm_id')
        action = message.get('action')

        if alarm_id and action:
            await self.change_alarm_status(alarm_id, action)
            await self.channel_layer.group_send(
                group=str(self.scope['user'].id),
                message={
                    'type': 'send_message',
                    'message': 'success'
                }
            )
        else:
            await self.channel_layer.group_send(
                group=str(self.scope['user'].id),
                message={
                    'type': 'send_message',
                    'message': 'echo message'
                }
            )

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def change_alarm_status(self, alarm_id, action):
        alarm = Alarm.objects.get(id=alarm_id)
        if action == 'read':
            alarm.has_read = True
        elif action == 'done':
            alarm.has_done = True
        alarm.save()
