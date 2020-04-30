from server.v1.url.util.crawling import Crawler
from rest_framework import generics
from server.models.url import Url, UrlSerializer
from server.models.category import Category
from server.exceptions import ServerException

class UrlListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = UrlSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user.pk
        category_id = self.request.data.get('category')
        url = self.request.data.get('url')
        if Category.objects.filter(id=category_id).exists():
            crawler = Crawler(url)
            html = crawler.get_html()
            response = crawler.parse_html(html)
            request.data['category'] = category_id
            request.data['user'] = user
            request.data['title'] = response['title']
            request.data['description'] = response['description']
            request.data['image'] = response['image']
            return self.create(request, *args, **kwargs)
        raise ServerException("해당 카테고리는 존재하지 않습니다.")

    def get_queryset(self):
        user = self.request.user
        category_id = self.request.data.get('category')
        category_queryset = Url.category.filter(id=category_id)
        user_queryset = Url.category.filter(user=user)


        return category_queryset, user_queryset

class UrlRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    def perfrom_destroy(self):
        pass
