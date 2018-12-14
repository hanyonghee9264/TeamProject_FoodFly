from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models.store import Store
from .serializers import StoreSerializer, StoreDetailSerializer


class CustomPaginator(PageNumberPagination):
    page_size = 10
    max_page_size = 1000


class StoreList(APIView):
    permission_classes = (
        permissions.AllowAny,
    )
    queryset = Store.objects.select_related('category', 'owner').prefetch_related('storeimage_set')
    serializer_class = StoreSerializer
    pagination_class = CustomPaginator

    def get(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(
            queryset,
            self.request,
            view=self
        )

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class StoreDetail(APIView):
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request, pk):
        store = Store.objects.prefetch_related('storeimage_set').get(pk=pk)
        serializer = StoreDetailSerializer(store)
        return Response(serializer.data, status=status.HTTP_200_OK)
