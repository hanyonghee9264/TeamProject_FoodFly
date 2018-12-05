from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models.order import Order
from store.models import Food
from .models.cart import Cart, CartItem
from .serializers import CartItemSerializer, OrderSerializer

User = get_user_model()


class CartItemList(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        items = cart.item.filter(is_ordered=False)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        food = Food.objects.get(pk=request.data.pop('food_pk'))
        serializer = CartItemSerializer(
            data={
                **request.data,
                'cart': cart,
            },
            context={
                'food': food,
            },
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        cart = Cart.objects.get(user=request.user)
        food = Food.objects.get(pk=request.data.get('food_pk'))
        item = CartItem.objects.get(
            cart=cart,
            food=food,
        )
        serializer = CartItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        food = get_object_or_404(Food, pk=request.data.get('food_pk'))
        cart.item.filter(food=food).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get(self, request):
        user = User.objects.get(username=request.user)
        order = user.order_set.filter(payment_status=False)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderSerializer(
            data=request.data,
            context={
                'request': request,
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        order = Order.objects.get(pk=request.data.get('order_pk'))
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
