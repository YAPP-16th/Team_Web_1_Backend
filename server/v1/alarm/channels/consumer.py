import json

from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

from server.models.alarm import Alarm
from urlink import settings

CHANNEL_LAYER = get_channel_layer()


@database_sync_to_async
def update_alarm_transmission_status(alarm):
    alarm.has_been_sent = True
    alarm.save()


def send_message(alarm):
    if settings.DEBUG:
        channel_layer = get_channel_layer()
    else:
        channel_layer = CHANNEL_LAYER

    group = str(alarm.user.id)
    async_to_sync(channel_layer.group_send)(
        group=group,
        message={
            'type': 'notify_alarm',
            'data': {
                'name': alarm.name,
                'category': alarm.category.name,
                'url': alarm.url.path,
                'reserved_time': str(alarm.reserved_time)
            }
        }
    )
    async_to_sync(update_alarm_transmission_status)(alarm)


class AlarmConsumer(AsyncConsumer):
    GROUP_LIST = []

    async def websocket_connect(self, event):
        print('connect', event)
        await self.channel_layer.group_add(
            group=str(self.scope['user'].id),
            channel=self.channel_name
        )

        self.GROUP_LIST.append(str(self.scope['user'].id))

        await self.send({
            'type': 'websocket.accept'
        })

        await self.send_past_alarms()

    async def websocket_disconnect(self, event):
        print('disconnected', event)
        await self.channel_layer.group_discard(
            group=str(self.scope['user'].id),
            channel=self.channel_name
        )

        self.GROUP_LIST.remove(str(self.scope['user'].id))

    async def websocket_receive(self, event):
        print('receive', event)
        await self.channel_layer.group_send(
            group=str(self.scope['user'].id),
            message={
                'type': 'notify_alarm',
                'data': json.loads(event['text']).get('message', '')
            }
        )

    async def notify_alarm(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(event)
        })

    async def send_past_alarms(self):
        past_alarms = await self.get_past_alarms(self.scope['user'])
        await self.channel_layer.group_send(
            group=str(self.scope['user'].id),
            message={
                'type': 'notify_alarm',
                'data': past_alarms
            }
        )

    @database_sync_to_async
    def get_past_alarms(self, user):
        results = []
        alarms = Alarm.objects.filter(user=user, has_been_sent=True)
        for alarm in alarms:
            results.append({
                'name': alarm.name,
                'category': alarm.category.name,
                'url': alarm.url.path,
                'reserved_time': str(alarm.reserved_time)
            })
        return results
