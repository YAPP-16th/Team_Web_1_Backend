import json

import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model

from server.models.user import UserSerializer
from server.v1.alarm.channels import send_message
from urlink.routing import application

TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


@database_sync_to_async
def get_user_with_token(username='hongjae', password='033156as!', email='bjq913@gmail.com'):
    user = get_user_model().objects.create_user(email, username, password)
    token = UserSerializer().get_token(user)['access']
    return user, token


@database_sync_to_async
def create_alarm(user):
    from server.models.category import Category
    from server.models.url import Url
    from server.models.alarm import Alarm
    from datetime import datetime, timezone
    reserved_time = datetime.strptime(str(datetime.now())[:16], '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)

    category = Category.objects.create(user=user, name="hi")
    url = Url.objects.create(user=user,
                             category=category,
                             path="abc.com",
                             title="hi",
                             description="aa",
                             image_path="hi")
    alarm = Alarm.objects.create(user=user,
                                 category=category,
                                 url=url,
                                 name="test",
                                 reserved_time=reserved_time)

    return alarm


@database_sync_to_async
def call_send_message_func(alarm):
    send_message(alarm, debug=True)


async def auth_connect(token):
    communicator = WebsocketCommunicator(application, f"/ws/connection/?token={token}")
    connected, subprotocol = await communicator.connect()
    assert connected is True
    return communicator


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class TestWebsockets:

    async def test_connect_websocket(self, settings):
        '''
        소켓연결이 되는지 테스트
        연결이되면 실행된 알람들이 반환되는데 지금 생성한 유저이므로 빈 배열이 반환되면 정상
        '''
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        user, token = await get_user_with_token()
        communicator = await auth_connect(token)

        response = await communicator.receive_json_from()
        data = response.get('message')
        assert data == []  # 초기에 전송된 알람이 없으므로 []가 반환된다.
        await communicator.disconnect()

    async def test_send_receive_message_from_consumer(self, settings):
        '''
        소켓을 연결한 후 서버에 메세지를 보내고 echo 되는지 테스트
        기능변경으로 다른 테스트로 대체 - 2020.06.15
        '''
        pass
        # settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        #
        # user, token = await get_user_with_token()
        # communicator = await auth_connect(token)
        # response = await communicator.receive_json_from()
        # assert response.get('message') == []
        #
        # await communicator.send_to(text_data=json.dumps({'message': 'This is a test message.'}))
        #
        # response = await communicator.receive_json_from()
        # data = response.get('message')
        # assert data == 'echo message'
        # await communicator.disconnect()

    async def test_send_message_func(self, settings):
        '''
        channels 패키지의 send_message()함수를 테스트한다.
        send_message() = 시간에 맞는 알람을 불러와서 알람을 등록한 사용자 그룹에 알람 메세지를 전송한다.
        '''
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        user, token = await get_user_with_token()
        communicator = await auth_connect(token)
        response = await communicator.receive_json_from()
        assert response.get('message') == []

        alarm = await create_alarm(user)
        assert alarm.name == 'test'

        await call_send_message_func(alarm)
        response = await communicator.receive_json_from()
        data = response.get('message')
        assert data.get('name') == 'test'
        await communicator.disconnect()

    async def test_send_action_message_to_change_alarm_status(self, settings):
        '''
        소켓을 연결한 후 서버에 메세지를 보내고 알람 상태가 변경되는지 테스트
        '''
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        user, token = await get_user_with_token()
        communicator = await auth_connect(token)
        await communicator.receive_json_from()

        # 알람 생성
        alarm = await create_alarm(user)

        await communicator.send_to(text_data=json.dumps({
            'alarm_id': str(alarm.id),
            'action': 'done'
        }))

        response = await communicator.receive_json_from()
        data = response.get('message')
        assert data == []
        await communicator.disconnect()
