from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response

from server.exceptions import ServerException
from server.models.category import Category
from server.models.url import Url, UrlSerializer
from server.permissions import IsOwner
from server.v1.url.utils.crawler import Crawler


class UrlListCreateAPIView(generics.ListCreateAPIView):
    # TODO 검색 필터링 해야한다.
    serializer_class = UrlSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user.pk
        category_id = self.request.query_params.get('category')
        urls = self.request.data.get('url')

        category = Category.objects.filter(id=category_id)
        if category.exists():
            response = []
            for url in urls:
                crawler = Crawler(url)
                html = crawler.get_html()
                parsed_html = crawler.parse_html(html)
                request.data['path'] = parsed_html['path']
                request.data['title'] = parsed_html['title'][:25]
                request.data['description'] = parsed_html['description'][:100]
                request.data['image_path'] = parsed_html['image_path']
                request.data['category'] = category_id
                request.data['user'] = user
                response.append(self.create(request, *args, **kwargs).data)
            return Response(response, status=status.HTTP_201_CREATED)
        raise ServerException("해당 카테고리는 존재하지 않습니다.")

    def get_queryset(self):
        user = self.request.user.pk
        category = self.request.query_params.get('category')
        queryset = Url.objects.filter(user=user, category=category)
        return queryset


class UrlDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UrlSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
