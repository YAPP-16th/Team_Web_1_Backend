from datetime import datetime
from random import randint


def get_delimiter(headers):
    '''
    websocket 이 연결될 때 유저의 header 정보들을 받아서 각 유저들을 구분할 수 있는 구분자를 반환한다.
    유저의 'sec-websocket-key' 를 구분자로 사용하는데 없을 경우 접속한 시간 + 랜덤숫자로 구분한다.
    '''

    def _parse():
        for header in headers:
            if header[0].decode('utf-8') == 'sec-websocket-key':
                return header[1].decode('utf-8')
        return f'{str(datetime.now())}{randint(1, 1000)}'

    return ''.join([i for i in _parse() if i.isalnum()])
