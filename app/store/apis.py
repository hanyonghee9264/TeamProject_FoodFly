from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

from .models.store import Store
from .serializers import StoreSerializer, StoreDetailSerializer


class CustomPaginator(PageNumberPagination):
    page_size = 10
    max_page_size = 1000


class StoreList(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = CustomPaginator
    lookup_url_kwarg = 'category_pk'

    def get_queryset(self):
        category = self.kwargs['category_pk']
        return Store.objects.filter(category=category).\
            select_related('category', 'owner'). \
            prefetch_related('storeimage_set', 'foodcategory_set', 'is_store_address_set')


class StoreDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StoreDetailSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_url_kwarg = 'store_pk'

    def get_queryset(self):
        store = self.kwargs['store_pk']
        return Store.objects.filter(pk=store). \
            select_related('category', 'owner'). \
            prefetch_related('storeimage_set', 'foodcategory_set', 'is_store_address_set')
