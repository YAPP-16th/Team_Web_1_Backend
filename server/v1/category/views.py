from django.db.models import F
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response

from server.models.category import Category, CategorySerializer
from server.permissions import IsOwner


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
        카테고리 리스트 or 등록 API

        ---

    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.filter(user=user)
        return queryset

    def get_my_last_order(self):
        return Category.objects.get_my_last_order(self.request)

    def post(self, request, *args, **kwargs):
        user = self.request.user.pk
        request.data['order'] = self.get_my_last_order() + 1
        request.data['user'] = user
        return self.create(request, *args, **kwargs)


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_destroy(self, instance):
        # 삭제할 시 order는 그 오더 밑에애들을 1씩 마이너스해준다.
        instance_order = instance.order
        Category.objects.filter(user=self.request.user, order__gt=instance_order).update(order=F('order') - 1)
        instance.delete()

    def update(self, request, *args, **kwargs):
        is_order_change = request.data.get('is_order_change')
        if is_order_change:
            new_order = request.data.get('new_order')
            obj = self.get_object()
            Category.objects.move(request, obj, new_order)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            super().update(request, *args, **kwargs)

    # TODO 1) db 실행계획, 인덱스 확인하기
