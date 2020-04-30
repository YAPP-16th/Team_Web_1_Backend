from django.db.models import F
from rest_framework import generics
from rest_framework import permissions

from server.models.category import Category, CategorySerializer
from server.permissions import IsOwner


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
        카테고리 리스트 or 등록 API

        ---
        ## Headers
            - Content type : application/json
            - Authorization : JWT <토큰>
        ## Body
            - name : 카테고리 이름

    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Category.objects.filter(user=user)
        return queryset

    def get_my_last_order(self):
        return Category.objects.get_my_last_order(self.request.user)

    def post(self, request, *args, **kwargs):
        user = self.request.user.pk
        request.data['order'] = self.get_my_last_order() + 1
        request.data['user'] = user
        return self.create(request, *args, **kwargs)


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        카테고리 조회 & 수정 & 삭제 API

        ---
        ## Headers
            - Content type : application/json
            - Authorization : JWT <토큰>
        ## Path Params
            - id : 카테고리 id
        ## Body
            - name : 카테고리 이름
            - order : 순서
            - is_favorited : 즐겨찾기

    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_destroy(self, instance):
        instance_order = instance.order
        Category.objects.filter(user=self.request.user, order__gt=instance_order).update(order=F('order') - 1)
        instance.delete()

    def update(self, request, *args, **kwargs):
        user = self.request.user.pk
        request.data['user'] = user
        return super().update(request, *args, **kwargs)

    # TODO 1) db 실행계획, 인덱스 확인하기
