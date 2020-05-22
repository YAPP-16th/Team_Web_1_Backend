import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# @receiver(post_save, sender=Alarm)
# def announce():
#     async_to_sync(channel_layer.group_send)(
#         "shares", {
#             "type": "share_message",
#             "message": "heelo",
#         }
#     )


class Consumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print('1')
        # print(message.reply_channel)
        async_to_sync(self.channel_layer.group_add)(
            self.groupname,
            self.channel_name
        )
    def connect(self):
        print('2')
        print(self.scope)
        channel_layer = get_channel_layer()
        async_to_sync(self.channel_layer.group_add)(
            self.groupname,
            self.channel_name
        )
        print(channel_layer)
        self.user = self.scope["user"]
        # Group("user-{}".format(user.id)).add(message.reply_channel)
        self.accept()
        if self.user.id == 1:
            self.send(text_data=json.dumps({
                'message': "hihii"
            }))

    def disconnect(self, close_code):
        self.close(close_code)

    # Receive message from room group
    def share_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
