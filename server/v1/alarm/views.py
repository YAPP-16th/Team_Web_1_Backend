from datetime import datetime

from rest_framework import generics
from rest_framework import permissions

from server.models.alarm import Alarm, AlarmSerializer
from server.permissions import IsOwner


class AlarmListCreateAPIView(generics.ListCreateAPIView):
    """
        알람 리스트 or 등록 API

        ---
        ## Headers
            - Content type : application/json
            - Authorization : JWT <토큰>
        ## Body
            - category : 카테고리 id
            - url : url id
            - reserved_time : 예약 시간
            - name : 알람명

    """
    serializer_class = AlarmSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Alarm.objects.filter(user=user)
        return queryset

    def post(self, request, *args, **kwargs):
        user = self.request.user.pk
        request.data['user'] = user
        request.data['reserved_time'] = datetime.strptime('{}-{}-{} {}:{}'.format(request.data['reserved_time']['year'],
                                                                                  request.data['reserved_time']['month'],
                                                                                  request.data['reserved_time']['day'],
                                                                                  request.data['reserved_time']['hour'],
                                                                                  request.data['reserved_time']['minute']),
                                                          '%Y-%m-%d %H:%M')

        return self.create(request, *args, **kwargs)


class AlarmRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
