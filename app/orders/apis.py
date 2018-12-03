from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models.cart import Cart
from .serializers import CartItemSerializer


class CartItemList(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        # cart = Cart.objects.get(pk=3)
        items = cart.item.filter(is_ordered=False)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        serializer = CartItemSerializer(
            data={
                **request.data,
                'cart': cart
            },
            context={
                'food_pk': request.data.pop('food'),
            },
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        pass

    def delete(self, request):
        pass


class OrderList(APIView):
    def post(self, request):
        pass
