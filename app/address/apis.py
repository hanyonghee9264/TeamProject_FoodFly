from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models import Address
from .serializers import AddressSerializer, AddressInfoSerializer


class UserAddressAPIView(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get(self, request):
        user = request.user
        serializer = AddressInfoSerializer(Address.objects.filter(user=user), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AddressSerializer(
            data={
                **request.data,
            },
            context={
                'request': request,
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        address_pk = request.data.get('address_pk')
        user = request.user
        if user.is_host_address_set.filter(pk=address_pk).exists():
            user.is_host_address_set.get(pk=address_pk).delete()
            serializer = AddressInfoSerializer(Address.objects.filter(user=user), many=True)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
