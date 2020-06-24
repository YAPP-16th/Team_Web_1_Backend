from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response

from server.exceptions import ServerException
from server.models.category import Category
from server.models.url import Url, UrlSerializer
from server.models.url import UrlFilter
from server.permissions import IsOwner
from server.v1.url.utils.crawler import Crawler


class UrlListCreateAPIView(generics.ListCreateAPIView):
    """
        URL 리스트 or 등록 API

        ---
        ## Headers
            - Content type : application/json
            - Authorization : JWT <토큰>
        ## Query Params
            - category : 카테고리 ID [필수]
            - path : url 주소 [검색을 위한 선택]
            - title : 제목 [검색을 위한 선택]
        ## Body
            - path : ["url 주소", ...]
    """
    serializer_class = UrlSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UrlFilter

    def get_queryset(self):
        user = self.request.user.pk
        category = self.request.query_params.get('category')
        queryset = Url.objects.filter(user=user, category=category)
        return queryset

    def _save(self, request, *args, **kwargs):
        crawler = Crawler()
        results = []
        for path in request.data.get('path', []):
            html = crawler.get_html(path)
            parsed_html = crawler.parse_html(html)
            request.data['path'] = path
            request.data['title'] = parsed_html['title'][:25]
            request.data['description'] = None if parsed_html['description'] == '알수없음' else parsed_html['description'][:100]
            request.data['image_path'] = parsed_html['image_path']
            request.data['favicon_path'] = parsed_html['favicon_path']
            results.append(self.create(request, *args, **kwargs).data)
        return results

    def post(self, request, *args, **kwargs):
        category_id = self.request.query_params.get('category')
        category = Category.objects.filter(id=category_id)
        if category.exists() and len(category) == 1 and category[0].user == self.request.user:
            request.data['category'] = category_id
            request.data['user'] = self.request.user.pk
            results = self._save(request, *args, **kwargs)
            if results:
                return Response(results, status=status.HTTP_201_CREATED)
            raise ServerException("URL이 존재하지 않습니다.")
        raise ServerException('카테고리가 존재하지 않거나 해당 카테고리에 대한 권한이 존재하지 않습니다.')


class UrlRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
        URL 삭제 API

        ---
        ## Headers
            - Content type : application/json
            - Authorization : JWT <토큰>
        ## Path Params
            - id : URL ID
    """
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def put(self, request, *args, **kwargs):
        raise ServerException('PUT Method는 허용되지 않습니다.')
