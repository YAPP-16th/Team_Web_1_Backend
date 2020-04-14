from rest_framework import generics
from rest_framework import permissions

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

    #  삭제어쩌지?
