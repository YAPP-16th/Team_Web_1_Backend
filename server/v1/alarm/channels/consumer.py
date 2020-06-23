import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from server.models.alarm import Alarm
from server.v1.alarm.channels.utils import get_delimiter
from urlink.settings import REDIS


class AlarmConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = str(self.scope['user'].id)
        delimiter = get_delimiter(self.scope['headers'])
        self.group_id = f"{user_id}{delimiter}"

        await self.channel_layer.group_add(
            group=self.group_id,
            channel=self.channel_name
        )

        REDIS.lpush(user_id, self.group_id)

        await self.accept()
        await self.send_past_alarms()

    async def send_past_alarms(self):
        past_alarms = await self.get_past_alarms(self.scope['user'])
        await self.channel_layer.group_send(
            group=self.group_id,
            message={
                'type': 'send_message',
                'message': past_alarms,
                'status': 'initial'
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
                'url_favicon_path': alarm.url.favicon_path,
                'alarm_has_read': alarm.has_read,
                'alarm_has_done': alarm.has_done,
            })
        return results

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            group=self.group_id,
            channel=self.channel_name
        )
        user_id = str(self.scope['user'].id)
        REDIS.lrem(user_id, 1, self.group_id)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            message = json.loads(text_data)
            alarm_id = message.get('alarm_id')
            action = message.get('action')

            if alarm_id and action and action in ['read', 'done']:
                await self.change_alarm_status(alarm_id, action)
        except Exception as e:
            await self.close()
        else:
            user_id = str(self.scope['user'].id)
            user_group_list = REDIS.lrange(user_id, 0, -1)
            past_alarms = await self.get_past_alarms(self.scope['user'])
            if user_group_list:
                for user_group in user_group_list:
                    group = user_group.decode('utf-8')
                    await self.channel_layer.group_send(
                        group=group,
                        message={
                            'type': 'send_message',
                            'message': past_alarms,
                            'status': 'update'
                        }
                    )

    async def send_message(self, event):
        message = event['message']
        status = event['status']
        await self.send(text_data=json.dumps({
            'message': message,
            'status': status
        }))

    @database_sync_to_async
    def change_alarm_status(self, alarm_id, action):
        alarm = Alarm.objects.get(id=alarm_id)
        if action == 'read':
            alarm.has_read = True
        elif action == 'done':
            alarm.has_done = True
        alarm.save()
