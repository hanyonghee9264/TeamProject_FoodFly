from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Store
from .serializers import StoreSerializer


class StoreList(APIView):
    def get(self, request):
        store = Store.objects.select_related('owner').prefetch_related('food_set')
        serializer = StoreSerializer(store, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreDetail(APIView):
    def get(self, request, pk):
        store = Store.objects.get(pk=pk)
        serializer = StoreSerializer(store)
        return Response(serializer.data, status=status.HTTP_200_OK)