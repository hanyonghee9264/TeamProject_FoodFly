from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models.store import Store
from .serializers import StoreSerializer, StoreDetailSerializer


class StoreList(APIView):
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request):
        store = Store.objects.select_related('category', 'owner').prefetch_related('storeimage_set')
        serializer = StoreSerializer(store, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreDetail(APIView):
    permission_classes = (
        permissions.AllowAny,
    )

    def get(self, request, pk):
        store = Store.objects.prefetch_related('storeimage_set').get(pk=pk)
        serializer = StoreDetailSerializer(store)
        return Response(serializer.data, status=status.HTTP_200_OK)
