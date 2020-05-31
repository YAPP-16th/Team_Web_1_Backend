import json

from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

from server.models.alarm import AlarmMessage

CHANNEL_LAYER = get_channel_layer()


def send_message(alarm):
    group = str(alarm.user.id)
    async_to_sync(CHANNEL_LAYER.group_send)(
        group=group,
        message={
            'type': 'send_message',
            'data': {
                'name': alarm.name,
                'category': alarm.category.name,
                'url': alarm.url.path,
            }
        }
    )
    # 여기서 메시지 저장
    AlarmMessage.objects.create(user=alarm.user, alarm=alarm, message=alarm.name)


@database_sync_to_async
def get_alarm_messages(user):
    alarm_messages = AlarmMessage.objects.filter(user=user)
    return [i.message for i in alarm_messages]


class EchoConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connect', event)
        await self.channel_layer.group_add(
            group=str(self.scope['user'].id),
            channel=self.channel_name
        )
        # 접속하면 여기서 뿌려줘도 될듯? 따로 api 안만들고
        await self.send({
            'type': 'websocket.accept'
        })

        try:
            alarm_message = await get_alarm_messages(self.scope['user'])
            if alarm_message:
                await self.channel_layer.group_send(
                    group=str(self.scope['user'].id),
                    message={
                        'type': 'send_message',
                        'text': alarm_message
                    }
                )
        except Exception as e:
            print(e)

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    async def send_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(event)
        })
