import json
from datetime import datetime

from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework import generics
from rest_framework import permissions

from server.exceptions import ServerException
from server.models.alarm import Alarm, AlarmSerializer
from server.permissions import IsOwner


def index(request):
    return render(request, 'alarm/index.html', {})


def room(request, room_name):
    return render(request, 'alarm/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


class AlarmListCreateAPIView(generics.ListCreateAPIView):
    """
        알람 리스트 or 등록 API

        ---
        ## Headers
            - Content type : application/json
            - Authorization : JWT <토큰>
        ## Query Params
            - category : 카테고리 ID [필수]
            - url : URL ID [필수]
        ## Body
            - reserved_time : {"year": "연도", "month": "월", "day": "일", "hour": "시간(24시간 형식)", "minute": "분"}
                - 05월 == 5월, 3분 == 03분 - "0" 유무 상관 X
            - name : 알람명
    """
    serializer_class = AlarmSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Alarm.objects.filter(user=user)
        return queryset

    def post(self, request, *args, **kwargs):
        user = self.request.user.pk
        category_id = self.request.query_params.get('category')
        url_id = self.request.query_params.get('url')
        request.data['user'] = user
        request.data['category'] = category_id
        request.data['url'] = url_id
        request.data['reserved_time'] = self.reformat_string_to_datetime(request.data.get('reserved_time'))

        return self.create(request, *args, **kwargs)

    @staticmethod
    def reformat_string_to_datetime(time):
        try:
            _datetime = datetime.strptime(
                f"{time['year']}-{time['month']}-{time['day']} {time['hour']}:{time['minute']}",
                '%Y-%m-%d %H:%M')
        except Exception as e:
            raise ServerException('예약시간 형식이 올바르지 않습니다.')
        else:
            return _datetime


class AlarmDestroyAPIView(generics.DestroyAPIView):
    """
        Alarm 삭제 API

        ---
        ## Headers
            - Content type : application/json
            - Authorization : JWT <토큰>
        ## Path Params
            - id : Alarm ID
    """
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
