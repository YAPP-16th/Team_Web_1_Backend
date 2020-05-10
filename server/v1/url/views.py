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

    def post(self, request, *args, **kwargs):
        user = self.request.user.pk
        category_id = self.request.query_params.get('category')
        paths = self.request.data.get('path')

        category = Category.objects.filter(id=category_id)
        if category.exists():
            response = {'success': [], 'fail': []}
            crawler = Crawler()
            for path in paths:
                # TODO
                #  시간을 줄일방법이 없는지?
                #  이쪽 소스를 들어낼 수 없는지?
                #  메세지큐??
                try:
                    html = crawler.get_html(path)
                    parsed_html = crawler.parse_html(html)
                    request.data['path'] = path
                    request.data['title'] = parsed_html['title'][:25]
                    request.data['description'] = parsed_html['description'][:100]
                    request.data['image_path'] = parsed_html['image_path']
                    request.data['category'] = category_id
                    request.data['user'] = user
                    response['success'].append(self.create(request, *args, **kwargs).data)
                except ServerException as exception:
                    response['fail'].append({
                        'path': path,
                        'reason': exception.message
                    })
            if not response['success']:
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            return Response(response, status=status.HTTP_201_CREATED)
        raise ServerException("해당 카테고리는 존재하지 않습니다.")


class UrlDestroyAPIView(generics.DestroyAPIView):
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
